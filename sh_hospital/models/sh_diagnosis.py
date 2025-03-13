# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Diagnosis(models.Model):
    _name = 'sh.diagnosis'
    _description = 'Diagnosis Details'
    
    name = fields.Char("Name of  Diagnosis")