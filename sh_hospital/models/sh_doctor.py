# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class Doctor(models.Model):
    _name = 'sh.doctor'
    _description = 'Doctor'
    
    name = fields.Char("Name of Doctor")
    specialization = fields.Char("Specialization")
    patient_ids = fields.One2many('sh.patient', 'doctor_id', string="PatientIDs")
    
    # uid = fields.Char("Doctor's UID")
    
    
    @api.model_create_multi
    def create(self, vals_list):
        # print("Values",vals_list)
        # print("Self",self)
        # for val in vals_list:
        #     val['name'] = 'Dhruv'
        res = super(Doctor, self).create(vals_list)
        # print("\n\n\n\n\n\n==================================================",res)
        
        res.name = 'XYZ'
        return res
    
    # def write(self, vals_list):
    #     print("Values",vals_list)
    #     print("Self",self)
    #     print("\n\n\n\n\n\n==================================================",vals_list)
    #     vals_list['name'] = 'Dhruvv'
    #     res = super(Doctor, self).write(vals_list)
        
    #     return res