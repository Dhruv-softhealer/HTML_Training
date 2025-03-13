# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models,fields,api


class Category(models.Model):
    _name = "sh.employee.category"
    _description = "Employee Category Table"

    name = fields.Char("Category Name",required=True)
    active = fields.Boolean()
    color = fields.Integer("Color")

    # Many to Many Fields
    employee_ids = fields.Many2many(comodel_name="sh.employee")

class Job(models.Model):
    _name = 'sh.job'
    _description = "Job Description"

    name = fields.Char()
    active = fields.Boolean()

    # Many to One Fields
    manager_id = fields.Many2one(comodel_name="sh.employee", string="Job Manager")
    address_id = fields.Many2one(comodel_name="res.partner", string="Address")
    department_id = fields.Many2one(comodel_name="sh.department",string="Department")

    # One to Many Fields
    employees_ids = fields.One2many(comodel_name="sh.employee",inverse_name="job_id",string="Employees")

    # Many to Many Fields
    favorite_user_ids = fields.Many2many(comodel_name="res.users",column1="job_id",column2="fav_user_id")
    interviewers_ids = fields.Many2many(comodel_name="res.users",relation="sh_interviews")
    extended_interviewers_ids = fields.Many2many(comodel_name="res.users",relation="sh_extended_interviews")

class Employee(models.Model):
    _name = "sh.employee"
    _description = "Employee Description"

    name = fields.Char("Employee Name")

    # Many to One fields
    user_id = fields.Many2one(comodel_name="res.users",string="Odoo User Id")
    country_id = fields.Many2one(comodel_name="res.country",string="Country")
    country_of_birth = fields.Many2one(comodel_name="res.country",string="Country of birth")
    job_id = fields.Many2one(comodel_name="sh.job",string="Job Position")
    department_id = fields.Many2one(comodel_name="sh.department",string="Department",related="job_id.department_id")

class Department(models.Model):
    _name = 'sh.department'
    _description = "Department Description"

    name = fields.Char("Department Name",required=True)
    complete_name = fields.Char("Department Path",compute='_compute_complete_name', recursive=True)
    active = fields.Boolean()

    # Many to one fields
    parent_id = fields.Many2one(comodel_name="sh.department",string="Parent Department")
    manager_id = fields.Many2one(comodel_name="sh.employee",string="Manager")

    # One to Many fields
    childs_ids = fields.One2many(comodel_name="sh.department",inverse_name="parent_id",string="Child Department",automatic=True)
    jobs_ids = fields.One2many(comodel_name="sh.job",inverse_name="department_id")
    members_ids = fields.One2many(comodel_name='sh.employee',inverse_name="department_id")

    

    @api.depends('name', 'parent_id.name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s/%s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name


   


