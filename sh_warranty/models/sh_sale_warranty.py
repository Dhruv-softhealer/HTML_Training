# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import models,fields,api
from datetime import timedelta

class SaleWarrenty(models.Model):
    _name = 'sh.sale.warranty'

    name = fields.Char()
    sale_order_id = fields.Many2one('sale.order',readonly=True)
    warranty_period = fields.Integer(string='Warranty Period (in Month)',default=12)
    warranty_expiry_date = fields.Date(compute='_compute_expiry_date')

    @api.depends('sale_order_id.date_order')
    def _compute_expiry_date(self):
        for rec in self:
            if rec.sale_order_id.warranty_applicable and rec.sale_order_id.date_order:
                rec.warranty_expiry_date = (rec.sale_order_id.date_order + timedelta(days=30.4*rec.warranty_period))
            else:
                rec.warranty_expiry_date = None

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            sale_order = self.env['sale.order'].browse([vals['sale_order_id']])
            rec = super(SaleWarrenty,self).create(vals)
            rec.name = f'{rec.id:04}/{sale_order.partner_id.name}'
            return rec
        
    def unlink(self):
        for rec in self:
            res = self.env['sale.order'].browse([rec.sale_order_id.id])
            print("\n\n\n\n=======",res)
            res.warranty_applicable = False

        return super().unlink()

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warranty_ids = fields.One2many('sh.sale.warranty', 'sale_order_id', string='WarrentyIDs')
    warranty_applicable = fields.Boolean(default=False)
    expire_date_warranty = fields.Date(related='warranty_ids.warranty_expiry_date')

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            rec = super(SaleOrder,self).create(vals)
            if rec.warranty_applicable:
                self.env['sh.sale.warranty'].create([{
                    'sale_order_id' : rec.id,
                }])
            return rec

    @api.onchange('warranty_applicable')
    def _change_warranty(self):
        if not self.warranty_applicable:
            self.env['sh.sale.warranty'].search([('sale_order_id','=',self._origin.id)]).unlink()
        elif self.warranty_applicable:
            self.env['sh.sale.warranty'].create([{
                'sale_order_id' : self._origin.id,
            }])