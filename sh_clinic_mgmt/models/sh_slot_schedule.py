# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import exceptions, models, fields, api
from odoo.sql_db import timedelta

class SlotSchedule(models.Model):
    _name = 'sh.slot.schedule'
    _description = 'Slot Schedule'
    
    sh_schedule_id = fields.Many2one('sh.slots')
    # name = fields.Char()
    sh_appointment_line = fields.One2many('sh.appointment', 'sh_slot_id', string="Appointment")
    sh_date = fields.Date(string="Date", required=True)
    sh_start_time = fields.Float(string="Slot Start Time", required=True)
    sh_end_time = fields.Float(string="Slot End Time", required=True)
    
    def unlink(self):
        for line in self:
            if line.sh_schedule_id and line.sh_schedule_id.sh_cancel_time:
                hours = line.sh_schedule_id.sh_cancel_time
                cancel_deadline = line.create_date + timedelta(hours=hours)
                if fields.Datetime.now() > cancel_deadline:
                    raise exceptions.UserError(
                        f"You cannot delete this slot. Allowed cancel time is {hours} hours."
                    )
        return super(SlotSchedule, self).unlink()