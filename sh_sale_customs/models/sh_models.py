# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import fields, models

class Note(models.Model):
    _name = 'sh.note'
    _description = "Note Description"

    name = fields.Char('Note',required=True)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_note = fields.Many2many('sh.note')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_note = fields.Many2one('sh.note')