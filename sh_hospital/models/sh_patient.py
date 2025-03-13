# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Patient(models.Model):
    _name = 'sh.patient'
    _description = 'Patient Details'
    
    name = fields.Char("Name of Patient")
    age = fields.Integer("Patient Age")
    doctor_id = fields.Many2one('sh.doctor', string="DoctorID")
    diagnosis_ids = fields.Many2many('sh.diagnosis')
    