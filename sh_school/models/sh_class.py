# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class Class(models.Model):
    _name = 'sh.class'
    _description = "Class Management"
    
    
    clsline_ids = fields.One2many('sh.studentline', 'cls_id', string="CLS Lines")
    
    
    stu_ids = fields.One2many('sh.student','class_id', string="StudentIDs", ondelete='cascade')
    teacher_id = fields.Many2one('sh.teacher', string="TeacherID")
    name = fields.Char("Class Name")
    instructor_name = fields.Char("Instructor Name")
    description = fields.Text("Class Description")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    schedule = fields.Char("Schedule")
    room_num = fields.Integer("Room Number")
    status = fields.Selection([('active', 'Active'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], string="Class Status")
    class_type = fields.Selection([('lacture', 'Lacture'), ('lab', 'Lab')], string="Class Type")
    countstu = fields.Integer("Number of Student", compute="_compute_student")
    
    
    @api.depends("stu_ids")
    def _compute_student(self):
        for stu in self:
            stu.countstu = len(self.stu_ids)
            
