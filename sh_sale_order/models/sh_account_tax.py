# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Account_tax(models.Model):
    _name = 'sh.account.tax'
    _description = 'Account Tax Details'
    
    name = fields.Char("Name of Account")
