# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class CustomField(models.Model):
    _inherit = 'crm.lead'
    
    more_info = fields.Text(string='More Information')