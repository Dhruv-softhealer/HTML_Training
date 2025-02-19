# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models


class Category(models.Model):
    _name = "sh.employee.category"
    _description = "Employee Category Table"

    name = fields.Char("Category Name",required=True)
    active = fields.Boolean()
    color = fields.Integer("Color")

    # Many to Many Fields
    employee_ids = fields.Many2many('sh.emp.mngmt',string='EMP_IDs')