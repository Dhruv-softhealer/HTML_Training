# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

from odoo import models, fields, api
from odoo.exceptions import UserError

class ShAppointmentStageWizard(models.TransientModel):
    _name = 'sh.appointment.stage.wizard'
    _description = 'Change Stage Wizard'

    state = fields.Selection([
        ('new', 'New'),
        ('today_apt','Today'),
        ('in_progress', 'In Progress'),
        ('pending','Pending'),
        ('completed_appointment', 'Completed Appointment'),
        ('cancelled_appointment', 'Cancelled Appointment'),
    ], 
    default='new',
    tracking=True,
    )

    appointment_ids = fields.Many2many('sh.appointment', string="Appointments")

    def action_change_stage(self):
        model=self.env.context['active_model']
        ids=self.env.context['active_ids']
        print(f"\n\n\n\t--------------> 30 model",model)
        print(f"\n\n\n\t--------------> 31 ids",ids)
        rec=self.env[model].browse(ids)
        cancelled = rec.filtered(lambda r: r.sh_state == 'cancelled_appointment')
        if cancelled and self.state != 'cancelled_appointment':
            cancelled_names = ", ".join(cancelled.mapped('name'))
            raise UserError(
                f"You cannot change the stage of the following cancelled appointments:\n{cancelled_names}"
            )

        rec.write({'sh_state':self.state})
