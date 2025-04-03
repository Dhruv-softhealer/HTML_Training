# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api



class SaleSettingHistory(models.TransientModel):
    _inherit = ['res.config.settings']
    
    last_no_of_order = fields.Integer(string="Last No. Of Orders", related="company_id.last_no_of_order", readonly=False)
    last_no_of_days_order = fields.Integer(string="Last No. Of Day's Orders", related="company_id.last_no_of_days_order", readonly=False)
    stages = fields.Many2many('ir.model.fields.selection',string="Stages",domain=[('field_id.model', '=', 'sale.order'), ('field_id.name', '=', 'state')],related="company_id.stages",readonly=False)
    group_enable_reorder = fields.Boolean(string="Enable Reorder", related="company_id.group_enable_reorder", readonly=False, implied_group="sh_customer_sale_order_history.sh_order_history_access_group")
    
    

class AccessSetting(models.Model):
    _inherit = 'res.company'
    
    last_no_of_order = fields.Integer(string="Last No. Of Orders")
    last_no_of_days_order = fields.Integer(string="Last No. Of Day's Orders")
    stages = fields.Many2many('ir.model.fields.selection', domain=[('field_id.model', '=', 'sale.order'), ('field_id.name', '=', 'state')],store=True)
    group_enable_reorder = fields.Boolean(string="Enable Reorder")