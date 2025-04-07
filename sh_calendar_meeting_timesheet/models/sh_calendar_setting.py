# Part of Softhealer Technologies.

from odoo import models, fields, api



class CalendarSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    group_create_timesheet = fields.Boolean(string="Create Timesheet", related="company_id.group_create_timesheet", readonly=False, implied_group="sh_calendar_meeting_timesheet.sh_calendar_timesheet_access_group")
    
    
class AccessSetting(models.Model):
    _inherit = 'res.company'
    
    group_create_timesheet = fields.Boolean()