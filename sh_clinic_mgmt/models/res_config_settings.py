# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields
from datetime import date

class Setting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    
    sh_case_days = fields.Integer(string="Expired Case Days", related="company_id.sh_case_days", readonly=False)
    job_position_ids = fields.Many2many('hr.job',related='company_id.job_position_ids',readonly=False)
    
class AccessSetting(models.Model):
    _inherit = 'res.company'
    
    sh_case_days = fields.Integer()
    job_position_ids = fields.Many2many('hr.job', readonly=False)