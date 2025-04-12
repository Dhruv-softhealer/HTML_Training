# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import Command, models, fields, api


class CalendarTimesheet(models.Model):
    _inherit = 'calendar.event'
    
    reason = fields.Text(string="Reason")
    show_reason = fields.Boolean(string="Show Reason", default=False)
    sh_task_id = fields.Many2one('project.task', groups="sh_calendar_meeting_timesheet.sh_calendar_timesheet_access_group")
    sh_project_id = fields.Many2one('project.project', groups="sh_calendar_meeting_timesheet.sh_calendar_timesheet_access_group")
    timesheet_ids = fields.One2many('account.analytic.line','event_id', store=True)
    

    def _create_timesheet_entry(self, vals):
        if 'partner_ids' in vals.keys():
            for val in vals['partner_ids']:
                if val[0] == 4:
                    timesheet = self.env['account.analytic.line'].create({
                        'name': self.name,
                        'project_id': self.sh_project_id.id,
                        'partner_id': val[1],
                        'task_id': self.sh_task_id.id,
                        'unit_amount': self.duration,
                        'date': self.start,
                    })
                    self.timesheet_ids = [(4, timesheet.id)]
                elif val[0] == 3:
                        delete_timesheet = [p.id for p in self.timesheet_ids if p.partner_id.id == val[1]]
                        if len(delete_timesheet) == 1 :
                            self.timesheet_ids = [(2, delete_timesheet[0],0)]
                

    @api.model_create_multi    
    def create(self, vals):
        for val in vals:
            rec = super(CalendarTimesheet,self).create(val)
            if 'sh_project_id' or 'sh_task_id' or 'duration' or 'name' or 'start' or 'partner_ids' in val.keys():
                rec._create_timesheet_entry(val)
            return rec
    

    
    def write(self, vals):
        rec = super(CalendarTimesheet, self).write(vals)
        if 'sh_project_id' or 'sh_task_id' or 'duration' or 'name' or 'start' or 'partner_ids' in vals.keys():
            self._create_timesheet_entry(vals)
            # print(vals)
            if 'name' in vals.keys():
                self.timesheet_ids.write({'name': self.name})
            if 'sh_project_id' in vals.keys():
                self.timesheet_ids.write({'project_id': self.sh_project_id.id})
            if 'sh_task_id' in vals.keys():
                self.timesheet_ids.write({'task_id': self.sh_task_id.id})
            if 'start' in vals.keys():
                self.timesheet_ids.write({'date': self.start})
                self.show_reason = True
            if 'duration' in vals.keys():
                self.timesheet_ids.write({'unit_amount': self.duration})
        return rec