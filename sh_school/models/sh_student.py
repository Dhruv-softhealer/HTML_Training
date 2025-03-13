# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api
from odoo.exceptions import UserError


class Student(models.Model):
    _name = 'sh.student'
    _description = 'Student Management'

    # Basic Details....................
    
    stu_line = fields.One2many('sh.studentline','stud_id', string="Student Line")
    
    age_type = fields.Char("Age Type")
    class_id = fields.Many2one(related='stu_line.cls_id', ondelete='cascade', store=True, string="ClassID", readonly=False)
    name = fields.Char("Student Name")
    tname = fields.Char(related='class_id.teacher_id.name',string="Teacher's Name")
    image = fields.Image("Image")
    age = fields.Integer("Age")
    birthdate = fields.Date("Birthdate")
    enr_no = fields.Integer("Enrollment Number")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string="Gender")
    year_of_enroll = fields.Integer("Year of Enroll")
    email = fields.Char("Email")
    phone = fields.Char("Phone Number")
    city = fields.Char("City")
    postal = fields.Integer("Postal Code")
    state = fields.Char("State")
    country = fields.Char("Country")
    dist_from_school_in_m = fields.Float("Disctence from Schoole in Meter")
    dist_from_school_in_km = fields.Float("Disctence from Schoole in KM", compute="_compute_distence")

    # Academil Details.............

    grade = fields.Char("Grade")
    section = fields.Char("Section")
    roll_no = fields.Integer("Roll Number")
    clg_name = fields.Char("Collage Name")
    previous_school = fields.Char("Previous School")

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


    stu_name = fields.Char("Student Name")
    stu = fields.Many2one('res.users', string="Stu ID")
    tz = fields.Char("TimeZone")


    has_duplicate_mobile = fields.Boolean()


    @api.model_create_multi
    def create(self, vals_list):
        for rec in vals_list:
            record1 = self.env["sh.student"].search([('phone', '=', rec['phone'])])
            record2 = self.env['sh.student'].search([('email', '=', rec['email'])])
            if record1:
                rec['has_duplicate_mobile'] = False
                raise UserError('Duplicate phone number')

            if record2:
                raise UserError('Email already exist')
        
        return super(Student, self).create(vals_list)
        
   
        
    def write(self, vals_list):
        if '+91' not in vals_list['phone'][0:3]:
            vals_list['phone'] = '+91' + vals_list['phone']
        # print(vals_list['phone'])
        # print("\n\n\n\n\n\n",vals_list['phone'])
        # for rec in vals_list:
        record = self.env["sh.student"].search([('phone', '=', vals_list['phone'])])
        if record:
            # vals_list['has_duplicate_mobile'] = False
            raise UserError('Duplicate phone number')
        return super(Student, self).write(vals_list)

    @api.depends("dist_from_school_in_m")
    def _compute_distence(self):
        for dis in self:
            dis.dist_from_school_in_km = self.dist_from_school_in_m/1000
            
    @api.onchange("stu")
    def _onchange_stu(self):
        self.stu_name = self.stu.name
        self.tz = self.stu.tz
        
       
class Studentline(models.Model):
    _name = "sh.studentline"
    _description = "Student Line"
    
    cls_id = fields.Many2one('sh.class', string="Class Line")
    stud_id = fields.Many2one('sh.student', string="Student Name")
    
    # @api.model
    # def create(self,vals_list):
    #     vals_list = [vals_list]
    #     for rec in vals_list:
    #         record = self.env['sh.studentline'].search([('stud_id','=',rec['stud_id'])])

    #         if record:
    #             record.write({'cls_id':rec['cls_id']})
    #             return record
    #         else:
    #             return super(Studentline,self).create(vals_list)