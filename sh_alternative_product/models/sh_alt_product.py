# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api



class Alternative_Product(models.Model):
    _inherit = ['product.product']
    _description = 'Product Management'
    
    
    alt_product = fields.Many2many(
        comodel_name='product.product',
        relation='sh_alternative_product',
        column1='product_id',
        column2='alt_product_id',
        string="Alternative Product",
        groups='sh_alternative_product.sh_manage_alt_product'
    )
    # product_uom_qty = fields.Float()
    # price_unit = fields.Float()
    
    
    # @api.onchange('alt_product')
    # def onchange_product(self):
    #     for product in self.alt_product:
    #         prod_ids = [p._origin.id for p in self.alt_product if p._origin.id != product._origin.id] + [self._origin.id]
    #         product._origin.write({'alt_product':[(6,0,prod_ids)]})
            
            
    def _change_alternative_products(self,vals):
        
        for val in vals:
            prod_id = self.browse(val[1])
            
            # Link
            if val[0] == 4 :
                not_in_alt_id = self.search(domain= [
                                    ('id','not in',[rec.id for rec in self.alt_product]),
                                      ('id','in',[rec.id for rec in prod_id.alt_product]),
                                    ('id','!=',self.id)])
                print("\n\n\n\n",not_in_alt_id)
                super(Alternative_Product,self).write({'alt_product':[(4,prod_id.id)]})

                for alt_id in not_in_alt_id:
                    super(Alternative_Product,self).write({'alt_product':[(4,alt_id.id)]})
                    alt_id.write({'alt_product':[(4,self.id)]})

                if self not in prod_id.alt_product:
                    prod_id.write({'alt_product':[(4,self.id)]})

                    for alt_id in not_in_alt_id:
                        prod_id.write({'alt_product':[(4,alt_id.id)]})


            # Unlink
            if val[0] == 3:
                prod_id.write({'alt_product':[(5,0,0)]})
                self.env.execute_query(api.SQL(f"delete FROM sh_alternative_product WHERE alt_product_id={prod_id.id} ;"))

               

    def write(self, vals):
        if vals.get('alt_product'):
            self._change_alternative_products(vals['alt_product'])
        return super(Alternative_Product,self).write(vals) 