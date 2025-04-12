# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class MRP_Production(models.Model):
    _inherit = 'mrp.production'
    
    
    sh_checklist_completed = fields.Float(string="Checklist Completed", compute='_calculate_complete_percantage', readonly=False, store=True)
    sh_m2o_checklist_template = fields.Many2many('sh.mrp.custom.checklist.template', store=True, readonly=False)
    
    sh_o2m_checklist = fields.One2many('sh.mrp.checklist.line', 'checklist_id')
    
    
    @api.onchange('sh_m2o_checklist_template')
    def change_template(self):
        self.sh_o2m_checklist = [(5,0,0)]
        if self.sh_m2o_checklist_template.sh_checklist:
            for rec in self.sh_m2o_checklist_template.sh_checklist:
                # if rec.id not in self.sh_o2m_checklist.ids:
                dict1 = {'name':rec.name,'description':rec.description,'date':self.date_start,'state':'new'}
                self.sh_o2m_checklist = [(0,0,dict1)]
        
    @api.depends('sh_o2m_checklist.state')
    def _calculate_complete_percantage(self):
       for rec in self:
            completed = 0
            total = len(rec.sh_o2m_checklist)
            if total:
                completed = sum(1 for line in rec.sh_o2m_checklist if line.state == 'complete')
                print("\n\n\n----------------->",completed)
                rec.sh_checklist_completed = (completed / total) * 100
            else:
                rec.sh_checklist_completed = 0
        
