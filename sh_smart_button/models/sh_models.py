# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import fields,models

class Sale(models.Model):
    _inherit = "sale.order"

    product_count = fields.Integer(compute = "_count_product",default=0)
    def _count_product(self):
        self.product_count = len(self.order_line)

    def action_get_sales_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales',
            'view_mode': 'list',
            'res_model': 'product.template',
            'domain' : [("id","in",[id.id for id in self.order_line.product_template_id])],
            'context': "{'create': False}"
        }
    

class Customer(models.Model):
    _inherit = "res.partner"

    order_count = fields.Integer(compute="_count_orders",default=0)

    def _count_orders(self):
        self.order_count = len(self.sale_order_ids)

    def get_sales_orders(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : 'Orders',
            'view_mode' : 'list,form',
            'res_model' : 'sale.order',
            'domain' : [('id','in',[id.id for id in self.sale_order_ids])]
        }
    

class Employee(models.Model):
    _inherit = "hr.employee"

    def download_pdf(self):
        return