# Part of Softhealer Technologies.

from odoo import models, fields, api



class TimesheetSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    backdate_days_limit = fields.Integer(string="Restricted Timesheet After", related="company_id.backdate_days_limit", readonly=False)
    
    
class AccessSetting(models.Model):
    _inherit = 'res.company'
    
    backdate_days_limit = fields.Integer()