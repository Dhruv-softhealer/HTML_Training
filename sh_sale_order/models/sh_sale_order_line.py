# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Sale_Order_Line(models.Model):
    _name = 'sh.sale.order.line'
    _description = 'Sale Order Line Details'
    
    name = fields.Char("OrderLine Name")
    product_id = fields.Many2one("sh.product")
    tax_ids = fields.Many2many("sh.account.tax", string="TaxIDs")
    order_id = fields.Many2one("sh.sale.order", string="Order")