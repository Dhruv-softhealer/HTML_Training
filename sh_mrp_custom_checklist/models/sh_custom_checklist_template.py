# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class CustomChecklistTemplate(models.Model):
    _name = 'sh.mrp.custom.checklist.template'
    _description = 'MRP Custom Checklist Template'
    
    company_id = fields.Many2one('res.company')
    sequence = fields.Integer()
    name = fields.Char(string="Name")
    sh_checklist = fields.Many2many('sh.mrp.custom.checklist')