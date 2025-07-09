# -*- coding: utf-8 -*-
# Part of softhealer Technologies


from odoo import models, api
from odoo.exceptions import ValidationError,UserError
import xlsxwriter
import base64
from io import BytesIO

class PatientDemographicsWizard(models.TransientModel):
    _name = 'sh.patient.demographics.wizard'
    
    # ==================================================================
    #                       Generate PDF Format
    # ==================================================================

    def action_print_report(self):
        report_action = self.env.ref('sh_clinic_mgmt.action_patient_demographics_report').report_action(self)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action
    
    # ==================================================================
    #                       Generate Excel Format
    # ==================================================================
    
    def action_excel_report(self):
        report_data = self.env['report.sh_clinic_mgmt.patient_demographics_report_template']._get_report_values(self.ids)
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
        
        workbook = xlsxwriter.Workbook("/tmp/Patient_Demographics_Report.xlsx")
        worksheet = workbook.add_worksheet('Patient Demographics Report')

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

        title = "Patient Demographics Report"
        column_span = 5
        worksheet.merge_range(0, 0, 1, column_span - 1, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========

        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 15)
        
        # =========== >>>> Headers <<<< ===========

        headers = ["Age Group", "Male", "Female", "Other", "Total Patients"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('age_group', ''), normal_record)
            worksheet.write(row, 1, record.get('male', 0), normal_record)
            worksheet.write(row, 2, record.get('female', 0), normal_record)
            worksheet.write(row, 3, record.get('other', 0), normal_record)
            worksheet.write(row, 4, record.get('total_patients', 0), normal_record)
            row += 1

        filename = 'Patient_Demographics_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Patient_Demographics_Report.xlsx", 'rb').read())
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


class PatientDemographicsReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.patient_demographics_report_template'
    _description = 'Patient Demographics Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        query = '''
            SELECT
                CASE
                    WHEN sh_age::integer BETWEEN 0 AND 18 THEN '0-18'
                    WHEN sh_age::integer BETWEEN 19 AND 40 THEN '19-40'
                    WHEN sh_age::integer BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+'
                END AS age_group,
                SUM(CASE WHEN sh_gender = 'male' THEN 1 ELSE 0 END) AS male,
                SUM(CASE WHEN sh_gender = 'female' THEN 1 ELSE 0 END) AS female,
                SUM(CASE WHEN sh_gender = 'other' THEN 1 ELSE 0 END) AS other,
                COUNT(*) AS total_patients
            FROM
                res_partner
            WHERE
                sh_age IS NOT NULL
                AND sh_gender IS NOT NULL
            GROUP BY
                CASE
                    WHEN sh_age::integer BETWEEN 0 AND 18 THEN '0-18'
                    WHEN sh_age::integer BETWEEN 19 AND 40 THEN '19-40'
                    WHEN sh_age::integer BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+'
                END
            ORDER BY
                age_group;

        '''

        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'data': data or {},
            'results': results,
        }