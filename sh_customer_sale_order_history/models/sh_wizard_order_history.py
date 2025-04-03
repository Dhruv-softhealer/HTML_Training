# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api



class SaleOrderHistory(models.Model):
    _inherit = 'sale.order.line'
    
    is_selected = fields.Boolean()
    sh_order_id = fields.Many2one('sale.order')
    sh_date_order = fields.Datetime(compute="_compute_date_order", store=True)
    
    def _compute_date_order(self):
        for rec in self:
            rec.sh_date_order=rec.order_id.date_order
            
            
                
    def view_line_order(self):
        return {
                'type':'ir.actions.act_window',
                'res_model':'sale.order',
                'view_mode':'form',
                'res_id':self.order_id.id
            }
        
    def sync_line_btn(self):
        # print("\n\n\n\n",self.env.context.get('params'))
        # currant_id=self.env.context.get('params')('resId')
        vals = {
            'order_id':self.sh_order_id.id,
            'product_id':self.product_id.id,
            'price_unit':self.price_unit,
            'tax_id':self.tax_id,
        }
        self.create(vals)
        
        
