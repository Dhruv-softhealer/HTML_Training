# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import models,fields,api

class Tag(models.Model):
    _name = 'sh.tag'
    _description = 'Tag'
    
    
    name = fields.Char(string="Name")
    
class Task(models.Model):
    _name = 'sh.task'
    _description = 'Task'
    
    name = fields.Char(string='Name')
    amount = fields.Float(string='Amount')
    timesheet_id = fields.Many2one(comodel_name='sh.timesheet')
    

class Timesheet(models.Model):
    _name = 'sh.timesheet'
    _description = 'Timesheet'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    user_id = fields.Many2one(comodel_name='res.users')
    name = fields.Char(string='Name', tracking=True)
    description = fields.Html(string='Description')
    date = fields.Date(default=fields.datetime.now())
    hours = fields.Float(string='Hours')
    tag_ids = fields.Many2many('sh.tag', string='Tag IDs')
    state = fields.Selection([('draft', 'Draft'),
                              ('submitted', 'Submitted'),
                              ('approved', 'Approved'),
                              ('reject', 'Reject')],
                             default="draft")
    rejection_reason = fields.Text(string='Rejction Reason')
    task_ids = fields.One2many('sh.task','timesheet_id')
    total_amount = fields.Float(compute='_compute_total_amount')
    
    
    @api.depends('task_ids')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = 0
            for task in rec.task_ids:
                rec.total_amount += task.amount
                
    def action_view_invoice(self):
        print("\n\n\n\n\n\n=================Button called")
     
    def action_to_move_submitted(self):
        self.state = 'submitted'
        
    def action_to_move_approve(self):
        self.state = 'approved'
        
    def action_to_open_wizard(self):
        return{
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'sh.timesheet.rejection',
            'target' : 'new'
        }
    
    
class TimesheetRejection(models.TransientModel):
    _name = 'sh.timesheet.rejection'
    _description = "Timesheet Rejection Table"

    name = fields.Char('Rejection Reason',required=True)
    def timesheet_value(self):
        print(self.env.context)
        active_id = self.env.context.get('active_id')
        return active_id
    timesheet_id = fields.Many2one('sh.timesheet', default=timesheet_value)

    def submit_reason(self):
         active_model = self.env.context.get('active_model')
         active_id = self.env.context.get('active_id')
         timesheet_rec = self.env[active_model].browse([active_id])
         timesheet_rec.write({'rejection_reason':self.name,'state':'reject'})