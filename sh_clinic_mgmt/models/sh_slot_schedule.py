# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
from odoo import _, exceptions, models, fields, api
from odoo.sql_db import timedelta

class SlotSchedule(models.Model):
    _name = 'sh.slot.schedule'
    _description = 'Slot Schedule'
    
    sh_slot_id = fields.Many2one('sh.slots')
    name = fields.Char(string="Slot Number", readonly=True)
    sh_appointment_line = fields.Many2many('sh.appointment', string="Appointment", readonly=True)
    sh_date = fields.Date(string="Date", required=True)
    sh_start_time = fields.Float(string="Slot Start Time", required=True)
    sh_end_time = fields.Float(string="Slot End Time", required=True)
    
    

    # @api.depends('sh_date', 'sh_start_time')
    # def _compute_sh_datetime(self):
    #     for rec in self:
    #         if rec.sh_date and rec.sh_start_time is not None:
    #             hours = int(rec.sh_start_time)
    #             minutes = int((rec.sh_start_time - hours) * 60)
    #             rec.sh_date = datetime.combine(rec.sh_date, datetime.min.time()) + timedelta(hours=hours, minutes=minutes)
    #         else:
    #             rec.sh_date = False

    # Check if the slot can be deleted based on the cancel time
    
    def unlink(self):
        for line in self:
            if line.sh_slot_id and line.sh_slot_id.sh_cancel_time:
                hours = float(line.sh_slot_id.sh_cancel_time)
                
                cancel_deadline = line.create_date + timedelta(hours=hours)
                now = fields.Datetime.now()
                print(f"\n\n\n\t--------------> 38 create_date",now )
                now = fields.Datetime.now()

                if now > cancel_deadline:
                    raise exceptions.UserError(
                        f"Slots are already generated."
                    )

        return super(SlotSchedule, self).unlink()
    
    # sequence number for the slot schedule
    
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            
            # date = val.get('sh_date')
            start = val.get('sh_start_time')
            end = val.get('sh_end_time')
            slot_code = f"{start} to {end}"
            val['name'] = slot_code

        return super().create(vals)