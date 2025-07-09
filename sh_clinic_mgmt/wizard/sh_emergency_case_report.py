# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import xlsxwriter
import base64
from io import BytesIO

class EmergencyCasesReportWizard(models.TransientModel):
    _name = 'sh.emergency.cases.wizard'
    _description = 'Emergency Cases Report'

    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)

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
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_emergency_cases_report').report_action(self, data=data)
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
        report_data = self.env['report.sh_clinic_mgmt.emergency_cases_report_template']._get_report_values(self.ids, data=data)
        results = report_data.get('results', [])

        fp, filename = self.prepare_excel_report(results)

        return self.create_and_send_attachment(fp, filename)
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, results):
        
        # =========== >>>> create workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Emergency_Cases_Report.xlsx")
        worksheet = workbook.add_worksheet('Emergency Cases Report')
        
        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#B8B4B490', 'border': 1, 'color': 'white'
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 8, 'valign': 'vcenter', 'border': 1,'align': 'center',
        })

        title = f"Emergency Cases Report (From {self.from_date} to {self.to_date})"
        column_span = 4 
        worksheet.merge_range(0, 0, 1, column_span - 4, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 30)
        
        # =========== >>>> Header <<<< ===========
        
        worksheet.write(3, 0, "Emergency Cases", bold)

        # =========== >>>> Write Data <<<< ===========
        
        row = 4
        for record in results:
            emergency_count = record.get('emergency_count', 0)
            worksheet.write(row, 0, emergency_count, normal_record)
            row += 1

        filename = 'Emergency_Cases_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Emergency_Cases_Report.xlsx", 'rb').read())
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

class EmergencyCasesReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.emergency_cases_report_template'
    _description = 'Emergency Cases Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        query = '''
            SELECT
                COUNT(*) AS emergency_count
            FROM
                sh_appointment apt
            WHERE
                apt.sh_date BETWEEN %s AND %s
                AND apt.sh_emergency_case = TRUE;
        '''

        params = [from_date, to_date]
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.emergency.cases.wizard',
            'data': data,
            'results': results,
        }