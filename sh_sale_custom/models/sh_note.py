# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Note(models.Model):
    _name = 'sh.note'
    _description = 'Note'
    
    name = fields.Char(string='Name')
    
    
class SaleOrders(models.Model):
    _inherit = 'sale.order'
    
    custom_notes = fields.Many2many('sh.note')
    # count = fields.Char(string="Total")
    
    
class SaleOrderLines(models.Model):
    _inherit = 'sale.order.line'
    
    
    custom_note = fields.Many2one('sh.note')