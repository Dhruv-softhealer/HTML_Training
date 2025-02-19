# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class Teacher(models.Model):
    _name = 'sh.teacher'
    _description = "Teacher Management"
    
    class_ids = fields.One2many('sh.class','teacher_id', string="ClassIDs")
    name = fields.Char(string="Teacher Name")
    email = fields.Char("Email")
    phone = fields.Text("Phone Number")
    dob = fields.Date("Date of Birth")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    address = fields.Text("Address")
    hire_date = fields.Date("Hire Date")
    department = fields.Char("Department")
    status = fields.Selection([('active', 'Active'), ('retired', 'Retired')], string="Teacher Status")
    count = fields.Integer("Number of Classes", compute='_compute_count')
    total = fields.Integer("Total", compute='_compute_change', inverse='_inverse_change')
    amount = fields.Integer("Amount")


    @api.depends('class_ids')
    def _compute_count(self):
        for teacher in self:
            # print(len(self.class_ids),self.class_ids)
            teacher.count = len(teacher.class_ids)
        # self.amount = len(self.name)
        
        
    # @api.onchange('amount')
    # def _onchange_count(self):
    #     self.total = 2 * self.amount
    
    @api.depends('amount')
    def _compute_change(self):
        for test in self:
            test.total = 2 * test.amount

    # @api.depends('total')
    def _inverse_change(self):
        for test in self:
            test.amount = test.total/2