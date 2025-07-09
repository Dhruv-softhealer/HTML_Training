# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO
from dateutil import relativedelta

class MonthlyRevenueReportWizard(models.TransientModel):
    _name = 'sh.monthly.revenue.report'
    _description = 'Monthly Revenue Report'

    month = fields.Date(string='Month', required=True, default=lambda self: fields.Date.today().replace(day=1))

    @api.onchange('month')
    def onchange_month(self):
        if self.month and self.month.day != 1:
            self.month = self.month.replace(day=1)

    # ==================================================================
    #                       Generate PDF Format
    # ==================================================================

    def action_print_report(self):
        start_date = self.month.replace(day=1)
        end_date = start_date + relativedelta.relativedelta(months=1, days=-1)
        data = {
            'month': self.month.strftime('%B %Y'),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_monthly_revenue_report').report_action(self, data=data)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action

    # ==================================================================
    #                       Generate Excel Format
    # ==================================================================

    def action_excel_report(self):
        start_date = self.month.replace(day=1)
        end_date = start_date + relativedelta.relativedelta(months=1, days=-1)
        data = {
            'month': self.month.strftime('%B %Y'),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }
        report_data = self.env['report.sh_clinic_mgmt.monthly_revenue_report_template']._get_report_values(self.ids, data=data)
        results = report_data.get('results', [])

        fp, filename = self.prepare_excel_report(results)

        report_action = self.create_and_send_attachment(fp, filename)
        
        return report_action
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, results):
        
        # =========== >>>> Create Workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Monthly_Revenue_Report.xlsx")
        worksheet = workbook.add_worksheet('Monthly Revenue Report')

        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#B8B4B490', 'border': 1
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 8, 'valign': 'vcenter', 'border': 1, 'align': 'center'
        })

        title = f"Monthly Revenue Report - {self.month.strftime('%B %Y')}"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 7) + 1))
        worksheet.merge_range(0, 0, 1, column_span - 1, title, heading_format)
        
        # =========== >>>> Set column widths <<<< ===========
        
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 20)
        
        # =========== >>>> Headers <<<< ===========

        headers = ["Month", "Total Revenue", "Paid Amount", "Pending Amount", "Refunds"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('month', ''), normal_record)
            worksheet.write(row, 1, record.get('total_revenue', 0), normal_record)
            worksheet.write(row, 2, record.get('paid_amount', 0), normal_record)
            worksheet.write(row, 3, record.get('pending_amount', 0), normal_record)
            worksheet.write(row, 4, record.get('refunds', 0), normal_record)
            row += 1

        filename = 'Monthly_Revenue_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Monthly_Revenue_Report.xlsx", 'rb').read())
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

class MonthlyRevenueReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.monthly_revenue_report_template'
    _description = 'Monthly Revenue Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        month = data.get('month')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        query = '''
            SELECT
                %s AS month,
                COALESCE(SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total ELSE 0 END), 0) AS total_revenue,
                COALESCE(SUM(CASE WHEN ap.state = 'posted' AND am.move_type = 'out_invoice' THEN ap.amount ELSE 0 END), 0) AS paid_amount,
                COALESCE(SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_residual ELSE 0 END), 0) AS pending_amount,
                COALESCE(SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total ELSE 0 END), 0) AS refunds
            FROM
                account_move am
            LEFT JOIN
                account_payment ap ON am.id = ap.move_id
            WHERE
                am.state = 'posted'
                AND am.date BETWEEN %s AND %s
                AND (am.move_type = 'out_invoice' OR am.move_type = 'out_refund');
        '''

        params = [month, start_date, end_date]
        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.monthly.revenue.report',
            'data': data,
            'results': results,
        }