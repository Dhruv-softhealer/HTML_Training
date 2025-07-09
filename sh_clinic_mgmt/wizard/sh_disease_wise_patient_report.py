# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO

class DiseaseWisePatientReportWizard(models.TransientModel):
    _name = 'sh.disease.wise.patient.wizard'
    _description = 'Disease Wise Patient Report Wizard'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    disease_ids = fields.Many2many('sh.disease', string='Disease Name')

    @api.onchange('from_date', 'to_date')
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
            'disease_ids': self.disease_ids.ids if self.disease_ids else False,
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_disease_wise_patient_report').report_action(self, data=data)
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
            'disease_ids': self.disease_ids.ids if self.disease_ids else False,
        }
        report_data = self.env['report.sh_clinic_mgmt.disease_wise_patient_report_template']._get_report_values(self.ids, data=data)
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
        
        # =========== >>>> create workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Disease_Wise_Patient_Report.xlsx")
        worksheet = workbook.add_worksheet('Disease Wise Patient Report')

        # =========== >>>> Define formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 10, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#B8B4B490', 'border': 1, 'color': 'white'
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 9, 'valign': 'vcenter', 'border': 1, 'align': 'center'
        })

        title = f"Disease Wise Patient Report (From {self.from_date} to {self.to_date})"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 15) + 1))
        worksheet.merge_range(0, 0, 1, column_span - 3, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 25)
        worksheet.set_column(1, 1, 25)
        
        # =========== >>>> Header <<<< ===========

        headers = ["Disease Name", "Patient Count"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('disease_name', ''), normal_record)
            worksheet.write(row, 1, record.get('patient_count', 0), normal_record)
            row += 1

        filename = 'Disease_Wise_Patient_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Disease_Wise_Patient_Report.xlsx", 'rb').read())
        fp.seek(0)
        return fp, filename
    
    # =========== >>>> create Attachments <<<< ===========

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

class DiseaseWisePatientReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.disease_wise_patient_report_template'
    _description = 'Disease Wise Patient Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        disease_ids = data.get('disease_ids')

        query = '''
            SELECT
                sd.name AS disease_name,
                COUNT(DISTINCT apt.sh_patient_id) AS patient_count
            FROM
                sh_appointment apt
            JOIN
                sh_disease_detail sdl ON apt.id = sdl.sh_appointment_id
            JOIN
                sh_disease sd ON sdl.sh_disease_id = sd.id
            WHERE
                apt.sh_date BETWEEN %s AND %s
        '''

        params = [from_date, to_date]

        if disease_ids:
            placeholders = ', '.join(['%s'] * len(disease_ids))
            query += f' AND sdl.sh_disease_id IN ({placeholders})'
            params.extend(disease_ids)

        query += '''
            GROUP BY
                sd.name
            ORDER BY
                sd.name;
        '''

        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.disease.wise.patient.wizard',
            'data': data,
            'results': results,
        }