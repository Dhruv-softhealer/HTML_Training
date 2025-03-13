# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class A(models.Model):
    _name = 'a.a'
    
    
    a1 = fields.Char(string='Name')
    
class B(models.Model):
    # _name = 'b.b'
    _inherit = 'a.a'
    
    b1 = fields.Char(string='Name')
    c1 = fields.Char(string="Name")