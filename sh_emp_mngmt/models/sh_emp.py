# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Employee(models.Model):
    _name = 'sh.emp.mngmt'
    _description = 'Employee Management'

    name = fields.Char("Name", required=True)
    address = fields.Text("Address")
    age = fields.Integer("Age")
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], string="Gender")
    birthdate = fields.Date("Birthdate")
    marital_status = fields.Selection([('married', 'Married'),('unmarried', 'Unmarried')], string="Marital Status")
    nationality = fields.Char("Nationality")


    job_id = fields.Many2one('sh.job', string="JobID")
    department_id = fields.Many2one('sh.department', string="DepartmentID")

    user_id = fields.Many2one('res.users', string="UseerID")
    country_id = fields.Many2one('res.country', string="CountryID")
    country_of_birth = fields.Many2one('res.country', string="Country Of Birth")


    job_posotion = fields.Char("Job Posotion")
    department = fields.Char("Department")
    phone = fields.Integer("Phone")
    email = fields.Char("Email")
    work_email = fields.Char("Work Email")
    skills = fields.Text("Skills")

    image = fields.Image("Image")

    work_address = fields.Text("Work address")

    emg_name = fields.Char("Contact Name")
    emg_phone = fields.Integer("Contact Number")

    certificate = fields.Selection([('master', 'Master'), ('bechelor', 'Bechelor'), ('other', 'Other')], string="Certificate")
    field_of_study = fields.Char("Field of Study")
    school = fields.Char("School")

    security_num = fields.Integer("Social Security Number")
    pan_num = fields.Integer("Pan Number")
    bank_ac_num = fields.Integer("Bank A/C Number")

    emp_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Employee Status")
    leave_type = fields.Selection(
        [
            ('paid', 'Paid'),
            ('unpaid', 'Unpaid')
            ],
        string="Leave Type")