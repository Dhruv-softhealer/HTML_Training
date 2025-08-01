# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from datetime import date

class Setting(models.TransientModel):
    _inherit = 'res.config.settings'
    

    sh_allow_salesperson = fields.Boolean(related="pos_config_id.sh_pos_allow_salesperson", readonly=False, string="Allow Salesperson")
    