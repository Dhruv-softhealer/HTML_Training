# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class Replace_Product(models.TransientModel):
    _name = 'sh.replace.product'
    _description = 'Product Replacement'
    
    
    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    alternate_prod_id = fields.Many2many('product.product', string="Alternate Product")
    replace_prod_id = fields.Many2one('product.product', string="Replace Product")
    
    
    def replace_alternate_product(self):
        if self.replace_prod_id:
            active_model = self.env.context.get('active_model')
            active_id = self.env.context.get('active_ids')
            sale_order_line_id = self.env[active_model].browse(active_id)
            # print("\n\n\n\niddddddd : ",active_id)
            if sale_order_line_id:
                sale_order_line_id.product_id = self.replace_prod_id.id
                sale_order_line_id.price_unit = self.replace_prod_id.standard_price

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'
    
    def show_alternative_products(self):
        return{
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model' : 'sh.replace.product',
            'context' : {
                'default_product_id' : self.product_id.id,
                'default_alternate_prod_id' : [id.id for id in self.product_id.alt_product]
                },
            'target' : 'new',
        }
        