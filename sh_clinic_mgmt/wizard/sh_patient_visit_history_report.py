# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO

class PatientVisitHistoryWizard(models.TransientModel):
    _name = 'sh.patient.visit.history.wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    
    @api.onchange('from_date','to_date')
    def onchange_date(self):
        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                raise ValidationError("To date should be greater than from date.")

    # ==================================================================
    #                       Generate PDF Format
    # ==================================================================

    def action_print_report(self):
        data = {
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat(),
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_patient_visit_history_report').report_action(self, data=data)
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
        report_data = self.env['report.sh_clinic_mgmt.patient_visit_history_report_template']._get_report_values(self.ids, data=data)
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
        
        workbook = xlsxwriter.Workbook("/tmp/Patient_Visit_History_Report.xlsx")
        worksheet = workbook.add_worksheet('Patient Visit History Report')

        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter',
            'bg_color': '#B8B4B490', 'border': 1, 'color': 'white'
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 8, 'valign': 'vcenter', 'border': 1, 'align': 'center'
        })

        title = f"Patient Visit History Report (From {self.from_date} to {self.to_date})"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 20) + 1))
        worksheet.merge_range(0, 0, 1, column_span - 1, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        
        # =========== >>>> Headers <<<< ===========

        headers = ["Patient Name", "Total Visits", "Last Visit Date", "Assigned Doctor"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            doctor = self.env['hr.employee'].browse(record.get('doctor_name')).name if record.get('doctor_name') else ''
            worksheet.write(row, 0, record.get('patient_name', ''), normal_record)
            worksheet.write(row, 1, record.get('total_visits', 0), normal_record)
            worksheet.write(row, 2, record.get('last_visit_date').strftime('%Y-%m-%d') if record.get('last_visit_date') else '', normal_record)
            worksheet.write(row, 3, doctor, normal_record)
            row += 1

        filename = 'Patient_Visit_History_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Patient_Visit_History_Report.xlsx", 'rb').read())
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


class PatientVisitHistoryReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.patient_visit_history_report_template'
    _description = 'Patient Visit History Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        query = '''
            SELECT
            rp.id AS patient_id,
            rp.name AS patient_name,
            COUNT(*) AS total_visits,
            MAX(sa.sh_date) AS last_visit_date,
            sa.sh_doctor_id AS doctor_name
            FROM
                sh_appointment sa
            JOIN
                res_partner rp ON sa.sh_patient_id = rp.id
            WHERE
                sa.sh_date BETWEEN %s AND %s
                AND sa.sh_state = 'completed_appointment'
            GROUP BY
                rp.id, rp.name, sa.sh_doctor_id
            ORDER BY
                rp.name;
        '''

        params = [from_date, to_date]
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()
        
        return {
            'doc_ids': docids,
            'doc_model': 'sh.patient.visit.history.wizard',
            'data': data,
            'results': results,
        }
        