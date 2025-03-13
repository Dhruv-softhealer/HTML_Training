# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Sale_Order(models.Model):
    _name = 'sh.sale.order'
    _description = 'Sale Order Details'
    
    name = fields.Char("Order Ref")
    date = fields.Date("Order Date")
    partner_id = fields.Many2one("sh.res.partner", string="PartnerID")
    order_line_ids = fields.One2many("sh.sale.order.line", 'order_id', string="OrderLineIDs")