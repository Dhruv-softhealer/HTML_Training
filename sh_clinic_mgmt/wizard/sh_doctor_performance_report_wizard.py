# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO

class DoctorPerformanceReportWizard(models.TransientModel):
    _name = 'sh.doctor.performance.wizard'
    _description = 'Doctor Performance Report Wizard'

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
        report_action = self.env.ref('sh_clinic_mgmt.action_doctor_performance_report').report_action(self, data=data)
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
        report_data = self.env['report.sh_clinic_mgmt.doctor_performance_report_template']._get_report_values(self.ids, data=data)
        results = report_data.get('results', [])

        fp, filename = self.prepare_excel_report(results)

        report_action = self.create_and_send_attachment(fp, filename)
        
        return report_action
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, results):
        
        # =========== >>>> create workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Doctor_Performance_Report.xlsx")
        worksheet = workbook.add_worksheet('Doctor Performance Report')

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

        title = f"Doctor's Performance Report (From {self.from_date} to {self.to_date})"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 15) + 1))
        worksheet.merge_range(0, 0, 1, column_span, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 25)
        worksheet.set_column(3, 3, 25)
        worksheet.set_column(4, 4, 25)
        
        # =========== >>>> Headers <<<< ===========

        headers = ["Doctor Name", "Total Appointments", "Completed Appointments", "Cancelled Appointments", "Pending Appointments"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            doctor = self.env['hr.employee'].browse(record.get('doctor')).name
            worksheet.write(row, 0, doctor or '', normal_record)
            worksheet.write(row, 1, record.get('total', 0), normal_record)
            worksheet.write(row, 2, record.get('completed', 0), normal_record)
            worksheet.write(row, 3, record.get('cancelled', 0), normal_record)
            worksheet.write(row, 4, record.get('pending', 0), normal_record)
            row += 1

        filename = 'Doctor_Performance_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Doctor_Performance_Report.xlsx", 'rb').read())
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
    
    

class DoctorPerformanceReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.doctor_performance_report_template'
    _description = 'Doctor Performance Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        query = '''
            SELECT
                apt.sh_doctor_id AS doctor,
                COUNT(*) AS total,
                SUM(CASE WHEN apt.sh_state = 'completed_appointment' THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN apt.sh_state = 'cancelled_appointment' THEN 1 ELSE 0 END) AS cancelled,
                SUM(CASE WHEN apt.sh_state = 'pending' THEN 1 ELSE 0 END) AS pending
            FROM
                sh_appointment apt
            WHERE
                apt.sh_date BETWEEN %s AND %s
            GROUP BY
                apt.sh_doctor_id
            ORDER BY
                apt.sh_doctor_id;
        '''

        params = [from_date, to_date]
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.doctor.performance.wizard',
            'data': data,
            'results': results,
        }