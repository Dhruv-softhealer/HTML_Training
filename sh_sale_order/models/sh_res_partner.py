# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Res_Partner(models.Model):
    _name = 'sh.res.partner'
    _description = 'Partner Details'
    
    name = fields.Char("Name of partner")
    city = fields.Char("City")