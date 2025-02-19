# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Job(models.Model):
    _name = 'sh.job'
    _description = 'Job Management'

    name = fields.Char("Job Name")
    active = fields.Boolean("Is active or Not")
    manager_id = fields.Many2one('sh.emp.mngmt', string="ManagerID")
    address_id = fields.Many2one('res.partner', string="AddressID")
    department_id = fields.Many2one('sh.department', string="DepartmentID")
    
    emp_ids = fields.One2many(comodel_name='sh.emp.mngmt',inverse_name='job_id', string="EmployeeIDs")
    
    
    favorite_user_ids = fields.Many2many('res.users','res_abc', string="Favorite UserIDs")
    interviewer_ids = fields.Many2many('res.users','res_xyz', string="InterviewerIDs")
    extended_interviewer_ids = fields.Many2many('res.users', string="ExtendedInterviewerIDs")