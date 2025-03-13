# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class CustomField(models.Model):
    _inherit = 'crm.lead'
    
    more_info = fields.Text(string='More Information')
    
    k_name = fields.Char(compute='_kanban_field')
    
    tree_part = fields.Char(string="ABC", default="Kanban Field")
    
    
    # @api.depends
    def _kanban_field(self):
        for res in self:
            res.k_name = 'Kanban Field'