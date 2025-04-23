# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import datetime
from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

class Slots(models.Model):
    _name = 'sh.slots'
    _description = 'Slots'
    
    
    name = fields.Char(string="Slot Number", default=lambda self: _("New"))
    doctor_id = fields.Many2one('hr.employee', string="Doctor Name", required=True, tracking=True)
    sh_slot_time = fields.Float(string="Slot Time(In Min)", required=True)
    sh_allowed_patients = fields.Integer(string="Allowed Patients", tracking=True, required=True)
    sh_pre_booking = fields.Float(string="Pre-Booking Time(In Min)")
    sh_start_date = fields.Date(string="Start Date", required=True)
    sh_end_date = fields.Date(string="End Date", required=True)
    sh_cancel_time = fields.Float(string="Allow Cancelling(In Min)", required=True)
    
    sh_schedule_line = fields.One2many('sh.slot.schedule', 'sh_schedule_id', string="Appointment Slots")
    
    
    sh_state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('booked', 'Booked')
    ],default="draft")
    
    
    # ================================= SEQUENCE ==================================
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', ("New")) == ("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date'])
                ) if 'create_date' in vals else None
                vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
                    'sh.slots', sequence_date=seq_date) or _("New")
        return super().create(vals_list)
    
    
    # ================================= Date Constrain ==================================
    
    @api.constrains('sh_start_date', 'sh_end_date')
    def _check_date(self):
        for rec in self:
            if rec.sh_start_date and rec.sh_end_date:
                if rec.sh_end_date < rec.sh_start_date:
                    raise ValidationError("End Date cannot be earlier than Start Date.")