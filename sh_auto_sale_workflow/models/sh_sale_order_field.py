# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, Command


class SaleOrderWorkflow(models.Model):
    _inherit = 'sale.order'
    
    auto_sale_workflow = fields.Many2one('sh.auto.sale.workflow',groups='sh_auto_sale_workflow.sh_auto_sale_workflow_group_access' , string="Sale Workflow")
    # apply_auto_workflow = fields.Boolean()
    
    @api.model
    def default_get(self, fields_list):
        rtn = super(SaleOrderWorkflow, self).default_get(fields_list)
        var1=int(self.env['ir.config_parameter'].get_param('sh_auto_sale_workflow.auto_sale_workflow_m2o'))
        rtn.update({'auto_sale_workflow': var1 if var1 > 0 else False})
        return rtn
    
    @api.onchange('partner_id')
    def onchange_auto_sale_workflow(self):
        if self.partner_id.auto_sale_workflow:
            self.auto_sale_workflow = self.partner_id.auto_sale_workflow.id
    
    def action_confirm(self):
        res = super().action_confirm()
        if self.auto_sale_workflow:
            rec = self.env['sh.auto.sale.workflow'].browse(self.auto_sale_workflow.id)
            if rec.val_order:
                self.env['stock.picking'].search([('origin','=',self.name)]).button_validate()
                # self.env['stock.picking'].search([('id', 'in', rec.picking_ids.id)]).button_validate()
                if rec.force_transfer:
                    pass
                if rec.create_invoice:
                    var = self._create_invoices()
                    
                    if rec.val_invoice:
                        var.action_post()
                        
                        if rec.register_payment:
                            self.env["account.payment.register"].with_context(
                                active_model="account.move",
                                active_ids=var.id,
                                default_payment_method_line_id = self.auto_sale_workflow.payment_method.id,
                                default_journal_id = self.auto_sale_workflow.payment_journal.id
                                ).create({"group_payment": False}).action_create_payments()
                            
                            
                        if rec.send_invoice_by_email:
                            # self.env["account.move.send.wizard"].with_context(
                            #     active_model="account.move",
                            #     active_ids=var.ids,
                            #     mail_partner_ids=self.partner_id,
                            #     mail_subject=self.auto_sale_workflow.company_id
                            # ).action_send_and_print()
                            
                            self.env['account.move.send.wizard'].create([{"move_id": var.id}]).action_send_and_print()
        return res