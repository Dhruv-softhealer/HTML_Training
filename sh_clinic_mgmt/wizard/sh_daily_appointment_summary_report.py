# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from io import BytesIO
import base64
import xlsxwriter

 
class AppointmentSummaryReportWizard(models.TransientModel):
    _name = 'sh.appointment.summary.report.wizard'
    _description = 'Appointment Summary Report Wizard'
 
    sh_company_id = fields.Many2one('res.company',string='Company',default=lambda self:self.env.company)
 
    sh_doctor_domain_ids = fields.Many2many('hr.job',related='sh_company_id.job_position_ids',readonly=True)
    
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', domain="[('job_id', 'in', sh_doctor_domain_ids)]" , required=True)

    # =========== >>>> Date Validation <<<< ===========

    @api.onchange('from_date','to_date')
    def onchange_date(self):
        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                raise ValidationError("Please change the To date, that should be greater then from date")

    # ==================================================================
    #                        Generate PDF Report
    # ==================================================================

    def action_print_report(self):
        data = {
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat(),
            'doctor_id': self.doctor_id.id
        }
        report_action = self.env.ref('sh_clinic_mgmt.action_appointment_summary_report').report_action(self, data=data)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action
    
    # ==================================================================
    #                        Generate Excel Report
    # ==================================================================
    
    def action_excel_report(self):
        data = {
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat(),
            'doctor_id': self.doctor_id.id
        }
        report_data = self.env['report.sh_clinic_mgmt.appointment_summary_report_template']._get_report_values(self.ids, data=data)
        summary = report_data.get('summary', [])

        fp, filename = self.prepare_excel_report(summary)

        report_action = self.create_and_send_attachment(fp, filename)
     
        return report_action
    
    # ==================================================================
    #                       Prepare Excel Format
    # ==================================================================

    def prepare_excel_report(self, summary):
        
        # =========== >>>> create workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook("/tmp/Appointment_Summary_Report.xlsx")
        worksheet = workbook.add_worksheet('Appointment Summary Report')

        # =========== >>>> Define formats <<<< ===========
        
        heading_format = workbook.add_format({
            'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        bold = workbook.add_format({
            'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        normal_record = workbook.add_format({
            'font_size': 8, 'valign': 'vcenter', 'border': 1,'align': 'center'
        })
        
        doctor_name = self.doctor_id.name if self.doctor_id else 'All Doctors'
        title = f"Appointment Summary Report (From {self.from_date} to {self.to_date} | Doctor: {doctor_name})"
        title_length = len(title)
        column_span = max(1, min(10, (title_length // 15) + 1))
        worksheet.merge_range(0, 0, 1, column_span - 2, title, heading_format)

        # =========== >>>> Set column widths <<<< ===========
        
        column_widths = [20, 20, 20, 20, 20]
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width)

        # =========== >>>> Header <<<< ===========
        
        headers = ["Date", "Total Appointments", "Completed Appointments", "Cancelled Appointments", "Pending Appointments"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold)

        # =========== >>>> Write Data <<<< ===========
        
        row = 4
        for record in summary:
            worksheet.write(row, 0, record.get('date').strftime('%Y-%m-%d') if record.get('date') else '', normal_record)
            worksheet.write(row, 1, record.get('total', 0), normal_record)
            worksheet.write(row, 2, record.get('completed_appointment', 0), normal_record)
            worksheet.write(row, 3, record.get('cancelled_appointment', 0), normal_record)
            worksheet.write(row, 4, record.get('pending', 0), normal_record)
            row += 1

        filename = 'Daily_Appointment_Summary_Report.xlsx'
        fp = BytesIO()
        workbook.close()
        fp.write(open("/tmp/Appointment_Summary_Report.xlsx", 'rb').read())
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



class AppointmentSummaryReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.appointment_summary_report_template'
    _description = 'Appointment Summary Report'
 
    @api.model
    def _get_report_values(self, docids, data=None):
        # print(f"\n\n\n\t--------------> 9 data",data)
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        doctor_id = data.get('doctor_id')
 
        query_appointment = '''
            SELECT
                sh_date::DATE AS date,
                COUNT(*) AS total,
                SUM(CASE WHEN sh_state = 'completed_appointment' THEN 1 ELSE 0 END) AS completed_appointment,
                SUM(CASE WHEN sh_state = 'cancelled_appointment' THEN 1 ELSE 0 END) AS cancelled_appointment,
                SUM(CASE WHEN sh_state = 'pending' THEN 1 ELSE 0 END) AS pending,
                (
                    SUM(CASE WHEN sh_state = 'completed_appointment' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN sh_state = 'cancelled_appointment' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN sh_state = 'pending' THEN 1 ELSE 0 END)
                ) AS total
            FROM
                sh_appointment
            WHERE
                sh_date BETWEEN %s AND %s
                {doctor_filter}
            GROUP BY
                sh_date::DATE
            ORDER BY
                sh_date::DATE;
        '''
 
        doctor_filter = ''
        params = [from_date, to_date]
        if doctor_id:
            doctor_filter = 'AND sh_doctor_id = %s'
            params.append(doctor_id)
        query_appointment = query_appointment.format(doctor_filter=doctor_filter)

        self.env.cr.execute(query_appointment, params)
        results = self.env.cr.dictfetchall()
 
        summary = sorted(results, key=lambda x: x['date'])
        doctor = self.env['hr.employee'].browse(doctor_id) if doctor_id else None

        return {
            'doc_ids': docids,
            'doc_model': 'sh.appointment.summary.report.wizard',
            'data': data,
            'summary': summary,
            'doctor': doctor,
        }