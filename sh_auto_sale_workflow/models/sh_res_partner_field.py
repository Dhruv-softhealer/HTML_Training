# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class SaleOrderWorkflow(models.Model):
    _inherit = ['res.partner']
    
    auto_sale_workflow = fields.Many2one('sh.auto.sale.workflow', groups='sh_auto_sale_workflow.sh_auto_sale_workflow_group_access',  string="Sale Workflow")
    
