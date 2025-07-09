# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO

class MedicineStockReportWizard(models.TransientModel):
    _name = 'sh.medicine.stock.report'
    _description = 'Medicine Stock Report Wizard'

    medicine_id = fields.Many2one('product.product', string='Medicine Name', domain="[('type', '=', 'consu')]")

    # ==================================================================
    #                       Generate PDF  Format
    # ==================================================================

    def action_print_report(self):
        data = {
            'medicine_id': self.medicine_id.id if self.medicine_id else False,
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_medicine_stock_report').report_action(self, data=data)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action
    
    # ==================================================================
    #                       Generate Excel Format
    # ==================================================================

    def action_excel_report(self):
        data = {
            'medicine_id': self.medicine_id.id if self.medicine_id else False,
        }
        report_data = self.env['report.sh_clinic_mgmt.medicine_stock_report_template']._get_report_values(self.ids, data=data)
        results = report_data.get('results', [])
        print("Results structure:", results)

        fp, filename = self.prepare_excel_report(results)

        report_action = self.create_and_send_attachment(fp, filename)
       
        return report_action
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, results):
        
        # =========== >>>> Create Workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Medicine_Stock_Report.xlsx")
        worksheet = workbook.add_worksheet('Medicine Stock Report')

        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter',
            'bg_color': '#B8B4B490', 'border': 1, 'color': 'white'
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 9, 'valign': 'vcenter', 'border': 1, 'align': 'center'
        })

        medicine_name = self.medicine_id.name if self.medicine_id else 'All Medicines'
        title = f"Medicine Stock Report - {medicine_name}"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 15) + 1))
        worksheet.merge_range(0, 0, 1, column_span + 2, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 20)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 20)

        # =========== >>>> Headers <<<< ===========

        headers = ["Medicine Name", "On Hand Stock", "Expiry Date", "Reorder Level", "Status"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('medicine_name', '').get('en_US', ''), normal_record)
            worksheet.write(row, 1, record.get('on_hand_stock', 0), normal_record)
            worksheet.write(row, 2, record.get('expiry_date', 'N/A'), normal_record)
            worksheet.write(row, 3, record.get('reorder_level', 0), normal_record)
            worksheet.write(row, 4, record.get('status', ''), normal_record)
            row += 1

        filename = 'Medicine_Stock_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Medicine_Stock_Report.xlsx", 'rb').read())
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

class MedicineStockReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.medicine_stock_report_template'
    _description = 'Medicine Stock Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        medicine_id = data.get('medicine_id')

        query = '''
            SELECT
                pp.name AS medicine_name,
                COALESCE(SUM(sq.quantity), 0) AS on_hand_stock,
                NULL AS expiry_date,
                0 AS reorder_level,
                CASE
                    WHEN COALESCE(SUM(sq.quantity), 0) > 0 THEN 'In Stock'
                    ELSE 'Low Stock'
                END AS status
            FROM
                product_product pp
            JOIN
                product_template pt ON pp.product_tmpl_id = pt.id
            JOIN
                product_category pc ON pt.categ_id = pc.id
            LEFT JOIN
                stock_quant sq ON pp.id = sq.product_id
                AND sq.location_id IN (
                    SELECT id FROM stock_location WHERE usage = 'internal'
                )
            WHERE
                pc.name = 'Medicines'
                AND pp.active = TRUE
        '''
        params = []

        if medicine_id:
            query += ' AND pp.id = %s'
            params.append(medicine_id)

        query += '''
            GROUP BY
                pp.id, pt.name
            ORDER BY
                pt.name;
        '''

        self.env.cr.execute(query, params)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'sh.medicine.stock.report',
            'data': data,
            'results': results,
        }
