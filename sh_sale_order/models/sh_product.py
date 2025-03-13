# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Product(models.Model):
    _name = 'sh.product'
    _description = 'Product Details'
    
    name = fields.Char("Name of Product")