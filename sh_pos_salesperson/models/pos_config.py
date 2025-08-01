# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from datetime import date

class PosConfig(models.Model):
    _inherit = 'pos.config'
    

    sh_pos_allow_salesperson = fields.Boolean(string="Allow Salesperson")
    