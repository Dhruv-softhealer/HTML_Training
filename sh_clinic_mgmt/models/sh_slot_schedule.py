# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime
from odoo import _, exceptions, models, fields, api

class SlotSchedule(models.Model):
    _name = 'sh.slot.schedule'
    _description = 'Slot Schedule'
    
    sh_slot_id = fields.Many2one('sh.slots')
    name = fields.Char(string="Slot Number", readonly=True)
    sh_appointment_line = fields.Many2many('sh.appointment', string="Appointment", readonly=True)
    sh_date = fields.Date(string="Date", required=True)
    sh_start_time = fields.Float(string="Slot Start Time", required=True)
    sh_end_time = fields.Float(string="Slot End Time", required=True)
    

    # sequence number for the slot schedule
    
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            
            start = val.get('sh_start_time')
            end = val.get('sh_end_time')
            slot_code = f"{start} to {end}"
            val['name'] = slot_code

        return super().create(vals)
    
    
    