# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api


class Degree(models.Model):
    _name = 'sh.degree'
    _description = 'Degree of Students'

    name = fields.Char("Degree")
    stu_ids = fields.One2many('sh.student', 'degree_id', string="StudentID")



class Student(models.Model):
    _name = 'sh.student'
    _description = 'Student Management'

    # Basic Details....................
    degree_id = fields.Many2one('sh.degree', string="Degree")
    name = fields.Char("Student Name")
    description = fields.Char("Description", readonly=True)
    image = fields.Image("Image")
    age = fields.Integer("Age")
    birthdate = fields.Date("Birthdate")
    enr_no = fields.Integer("Enrollment Number")
    stu_id = fields.Text("Student ID")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string="Gender")
    year_of_enroll = fields.Integer("Year of Enroll")
    email = fields.Char("Email")
    phone = fields.Integer("Phone Number")
    city = fields.Char("City")
    postal = fields.Integer("Postal Code")
    state = fields.Char("State")
    country = fields.Char("Country")

    # Academil Details.............

    grade = fields.Char("Grade")
    section = fields.Char("Section")
    roll_no = fields.Integer("Roll Number")
    clg_name = fields.Char("Collage Name")
    previous_school = fields.Char("Previous School")
    total = fields.Integer(compute="_compute_total")
    amount = fields.Integer("Amount Based on total")

    # Parents Details.............

    father_name = fields.Char("Father's Name")
    mother_name = fields.Char("Mother's Name")
    parent_phone = fields.Integer("Parents Contact Number")
    parent_email = fields.Char("Parent's Email")
    emg_phone = fields.Integer("Emergency Contact Number")

    # Additional Details..........
    
    nationality = fields.Char("Nationality")
    blood = fields.Char("Blood Group")
    transport = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Use Transport?")
    date_of_admission = fields.Date("Date of Admission")


    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2 * record.amount
    
    @api.onchange("degree_id")
    def _onchange_degree_id(self):
        if self.degree_id:
            self.description = "Belongs from %s Degree" % (self.degree_id.name)
        else:
            self.description = ""
        
