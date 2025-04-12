# Part of Softhealer Technologies.

from odoo import models, fields, api



class CalendarSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    sh_select_project = fields.Many2one('project.project',string="Select Project", config_parameter='sh_helpdesk_ticket.sh_select_project')