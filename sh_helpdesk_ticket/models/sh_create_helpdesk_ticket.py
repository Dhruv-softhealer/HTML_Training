# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import Command, models, fields, api


class CalendarTimesheet(models.Model):
    _inherit = 'helpdesk.ticket'
    
    project_task_id = fields.Many2one('project.task', string='Related Task', readonly=True)

    def create_helpdesk_task(self):
        for ticket in self:
            project_id = self.env['ir.config_parameter'].sudo().get_param('sh_helpdesk_ticket.sh_select_project')
            project_id = int(project_id) if project_id else False

            if not project_id:
                raise api.UserError("No project selected in Settings.")

            task = self.env['project.task'].create({
                'name': ticket.name,
                'project_id': project_id
            })

            ticket.project_task_id = task.id

        return True