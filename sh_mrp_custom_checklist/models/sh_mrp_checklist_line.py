# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import Command, models, fields, api


class CustomChecklistLine(models.Model):
    _name = 'sh.mrp.checklist.line'
    _description = 'MRP Custom Checklist Line'
    
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    sequence = fields.Integer()
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    state = fields.Selection([('new', 'New'), ('complete', 'Complete'), ('cancel', 'Cancel')], string="State", default='new')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    
    checklist_id = fields.Many2one('mrp.production')
    
    
    # @api.onchange('name')
    # def onchange_name(self):
    #     for rec in self:
    #         rec.name=self.name
    #         rec.description = rec.name.description
    #         rec.state = 'new'
    
    def action_state_complete(self):
        for rec in self:
            rec.state = 'complete'
            
    def action_state_cancel(self):
        for rec in self:
            rec.state = 'cancel'