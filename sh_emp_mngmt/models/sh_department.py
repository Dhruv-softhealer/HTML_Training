# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Department(models.Model):
    _name = 'sh.department'
    _description = "Department"

    name = fields.Char("Department Name")
    active = fields.Boolean("Is Active or Not")
    parent_id = fields.Many2one('sh.department', string="parentID")
    manager_id = fields.Many2one('sh.emp.mngmt', string="ManagerID")
    
    
    child_ids = fields.One2many(comodel_name='sh.department',inverse_name='parent_id', string="ChildIDs")
    member_ids = fields.One2many(comodel_name='sh.emp.mngmt',inverse_name='department_id', string="MemberIDs")
    job_ids = fields.One2many(comodel_name='sh.job',inverse_name='department_id', string="JobIDs")