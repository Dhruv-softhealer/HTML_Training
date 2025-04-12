# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import Command, models, fields, api


class CustomChecklist(models.Model):
    _name = 'sh.mrp.custom.checklist'
    _description = 'MRP Custom Checklist'
    
    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    sequence = fields.Integer()
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)