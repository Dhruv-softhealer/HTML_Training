# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class Category(models.Model):
    _name = 'sh.category'
    _description = 'Category Details'
    
    c_line_ids = fields.One2many('sh.bookline', 'c_line_id', string="Class LineIDs")
        
    name = fields.Char("Category Name")
    description = fields.Text("Description")
    type = fields.Selection([('fiction', 'Fiction'), ('science', ' Science'), ('history', 'History')], string="Category Types")
    
    count = fields.Integer("Count of Total", compute="_count_books")
    ref = fields.Char("Reference ID", readonly=True)
    
    @api.depends('c_line_ids')
    def _count_books(self):
        for res in self:
            res.count = len(self.c_line_ids)
            
    @api.model_create_multi
    def create(self, vals_list):
        res = super(Category, self).create(vals_list)
        res.ref = f'{res.ref:3}'
        print("\n\n\n\n\n============", res['name'])
        return res