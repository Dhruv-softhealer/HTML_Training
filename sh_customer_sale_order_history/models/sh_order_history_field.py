# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import datetime
from odoo import Command, models, fields, api
from odoo.exceptions import UserError
from odoo.tools.convert import relativedelta



class SaleOrderHistory(models.Model):
    _inherit = 'sale.order'
    
    sale_order_history = fields.One2many('sale.order.line',inverse_name='sh_order_id',readonly=False  ,string="Order History")
    
    
    @api.onchange('partner_id')
    def _onchange_partner(self):
        day=self.company_id.last_no_of_days_order
        date=datetime.datetime.now() - relativedelta(days=day)
        rec=self.env['sale.order.line'].search(['&','&','&',('sh_date_order','>=',date),('state','in',([state.value for state in self.company_id.stages])),('order_id','!=',self._origin.id),('order_id.partner_id','=',self.partner_id.id)],limit=self.company_id.last_no_of_order,order="sh_date_order desc")
        self.sale_order_history=[Command.set(rec.ids)]
    
    
    @api.onchange("partner_id")
    def _get_order_history(self):
            self.sale_order_history = self.env['sale.order.line'].search(domain=[('order_partner_id','=',self.partner_id.id)])
                
    def reorder_line_btn(self):
        selected_lines = self.sale_order_history.search([('is_selected', '=', True)])
        print(selected_lines)
        if selected_lines:
            for rec in selected_lines:
                rec.sync_line_btn()
                rec.is_selected=False
        else:
            for rec in self.sale_order_history:
                rec.sync_line_btn()
                
                
    # def reorder_line_btn(self):
    #     selected_lines = self.sale_order_history.filtered(lambda line: line.is_selected)
        
    #     if not selected_lines:
    #         raise UserError("No lines selected for reorder.")

    #     new_order = self.create({
    #         'partner_id': self.partner_id.id,
    #         'state': 'draft',
    #     })

    #     for line in selected_lines:
    #         line.copy({'order_id': new_order.id})
    #         # line.unlink()

    #     return {
    #         'name': 'New Sale Order',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sale.order',
    #         'view_mode': 'form',
    #         'res_id': new_order.id,
    #         'target': 'current',
    #     }
        
        