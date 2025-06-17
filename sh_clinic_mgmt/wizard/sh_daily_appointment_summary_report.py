from odoo import models, fields

class AppointmentSummaryReportWizard(models.TransientModel):
    _name = 'sh.appointment.summary.report'
    _description = 'Appointment Summary Report'

    sh_company_id = fields.Many2one('res.company',string='Company',default=lambda self:self.env.company)

    # sh_doctor_domain_ids = fields.Many2many('hr.job',related='sh_company_id.job_position_ids',readonly=True)
    
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    doctor_id = fields.Many2one('hr.employee', string='Doctor', domain="[('job_id.name', '=', 'Doctor')]" , required=True)

    def action_print_report(self):
        data = {
            'from_date': fields.Date.to_string(self.from_date),
            'to_date': fields.Date.to_string(self.to_date),
            'doctor_id': self.doctor_id.id 
        }
        return self.env.ref('sh_clinic_mgmt.action_appointment_summary_report').report_action(self, data=data)
