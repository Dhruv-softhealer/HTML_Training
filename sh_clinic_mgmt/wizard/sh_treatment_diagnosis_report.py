# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO


class TreatmentDiagnosisWizard(models.TransientModel):
    _name = 'sh.treatment.diagnosis.wizard'
    _description = 'Treatment and Diagnosis Report'

    from_date = fields.Date(string='From Date', default=fields.Date.today, required=True)
    to_date = fields.Date(string='To Date', required=True,)

    @api.constrains('from_date', 'to_date')
    def _check_date_range(self):
        for record in self:
            if record.from_date > record.to_date:
                raise ValidationError('From Date must be before To Date.')
            
    # ==================================================================
    #                       Generate PDF Format
    # ==================================================================

    def action_print_report(self):
        data = {
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat(),
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_treatment_diagnosis_report').report_action(self, data=data)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action

    # ==================================================================
    #                       Generate Excel Format
    # ==================================================================

    def action_excel_report(self):
        data = {
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat(),
        }
        report_data = self.env['report.sh_clinic_mgmt.treatment_diagnosis_report_template']._get_report_values(self.ids, data=data)
        results = report_data.get('results', [])

        fp, filename = self.prepare_excel_report(results)

        report_action = self.create_and_send_attachment(fp, filename)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, results):
        
        # =========== >>>> Create Workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Treatment_Diagnosis_Report.xlsx")
        worksheet = workbook.add_worksheet('Treatment & Diagnosis Report')

        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#B8B4B490', 'border': 1, 'color': 'white'
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 9, 'valign': 'vcenter', 'border': 1, 'align': 'center'
        })

        title = f"Treatment & Diagnosis Report (From {self.from_date} to {self.to_date})"
        column_span = 4 
        worksheet.merge_range(0, 0, 1, column_span - 1, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)

        # =========== >>>> Headers <<<< ===========

        headers = ["Disease Name", "Total Cases", "Treated Successfully", "Ongoing Treatment"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('disease_name', ''), normal_record)
            worksheet.write(row, 1, record.get('total_cases', 0), normal_record)
            worksheet.write(row, 2, record.get('treated_successfully', 0), normal_record)
            worksheet.write(row, 3, record.get('ongoing_treatment', 0), normal_record)
            row += 1

        filename = 'Treatment_Diagnosis_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Treatment_Diagnosis_Report.xlsx", 'rb').read())
        fp.seek(0)
        return fp, filename

    # =========== >>>> Create Attachments <<<< ===========

    def create_and_send_attachment(self, fp, filename):
        IrAttachment = self.env['ir.attachment'].sudo()
        attachment = IrAttachment.search([
            ('name', '=', filename),
            ('type', '=', 'binary'),
            ('res_model', '=', 'ir.ui.view')
        ], limit=1)
        data = fp.read()
        base64_encoded = base64.b64encode(data).decode('UTF-8')
        attachment_vals = {
            'name': filename,
            'res_model': 'ir.ui.view',
            'type': 'binary',
            'datas': base64_encoded,
            'public': True,
        }
        fp.close()

        if attachment:
            attachment.sudo().write(attachment_vals)
        else:
            attachment = IrAttachment.sudo().create(attachment_vals)

        if not attachment:
            raise UserError('Failed to create attachment.')

        url = f"/web/content/{attachment.id}?download=true"
        return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}

class TreatmentDiagnosisReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.treatment_diagnosis_report_template'
    _description = 'Treatment and Diagnosis Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        query = '''
            WITH appointment_data AS (
                SELECT
                    sd.name AS disease_name,
                    COUNT(DISTINCT sdd.sh_disease_id) AS total_cases,
                    COUNT(DISTINCT CASE WHEN a.sh_state = 'completed_appointment' THEN a.id END) AS treated_successfully,
                    COUNT(DISTINCT CASE WHEN a2.sh_date >= CURRENT_DATE AND a2.sh_state NOT IN ('cancelled_appointment') THEN a2.id END) AS ongoing_treatment
                FROM
                    sh_disease_detail sdd
                JOIN
                    sh_disease sd ON sdd.sh_disease_id = sd.id
                JOIN
                    sh_appointment a ON sdd.sh_appointment_id = a.id
                LEFT JOIN
                    sh_appointment a2 ON a2.sh_patient_id = a.sh_patient_id
                WHERE
                    a.sh_date BETWEEN %s AND %s
                GROUP BY
                    sd.name
                ORDER BY
                    sd.name
            )
            SELECT
                disease_name,
                total_cases,
                treated_successfully,
                ongoing_treatment
            FROM
                appointment_data;
        '''

        params = [from_date, to_date]
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.treatment.diagnosis.wizard',
            'data': data,
            'results': results,
        }