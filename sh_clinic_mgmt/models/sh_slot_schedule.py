# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class SlotSchedule(models.Model):
    _name = 'sh.slot.schedule'
    _description = 'Slot Schedule'
    
    sh_schedule_id = fields.Many2one('sh.slots')
    sh_appointment_line = fields.One2many('sh.appointment', 'sh_slot_id', string="Appointment")
    sh_date = fields.Date(string="Date", required=True)
    sh_start_time = fields.Float(string="Slot Start Time", required=True)
    sh_end_time = fields.Float(string="Slot End Time", required=True)