# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class AutoSaleConfigWorkflow(models.TransientModel):
    _inherit = 'res.config.settings'
    
    auto_sale_config_bool = fields.Boolean(string="Enable Auto Workflow",default=False,implied_group='sh_auto_sale_workflow.sh_auto_sale_workflow_group_access', config_parameter='sh_auto_sale_workflow.auto_sale_config_bool')
    
    auto_sale_workflow_m2o = fields.Many2one('sh.auto.sale.workflow',implied_group='sh_auto_sale_workflow.sh_auto_sale_workflow_group_access', string="Default Workflow",config_parameter='sh_auto_sale_workflow.auto_sale_workflow_m2o')
    
    @api.model
    def set_values(self):
        super(AutoSaleConfigWorkflow, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("sh_auto_sale_workflow.auto_sale_config_bool", self.auto_sale_config_bool)

        group = self.env.ref('sh_auto_sale_workflow.sh_auto_sale_workflow_group_access', raise_if_not_found=False)
        if group:
            if self.auto_sale_config_bool:
                group.users = [(6,0, self.env['res.users'].search([]).ids)]
            else:
                group.users = [(5,0,0)]