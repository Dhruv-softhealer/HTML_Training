# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields, api

class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    sh_salesperson_id = fields.Many2one('res.users', string='Salesperson')

    
    def _load_pos_data_fields(self, config_id):
        res = super()._load_pos_data_fields(config_id)
        res.append('sh_salesperson_id')
        print(f"\n\n\n\t--------------> 28 res",res)
        return res
