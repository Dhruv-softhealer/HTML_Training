# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api



class AccountAnalytic(models.Model):
    _inherit = 'account.analytic.line'
    
    event_id = fields.Many2one('calendar.event')
    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one('project.project')
