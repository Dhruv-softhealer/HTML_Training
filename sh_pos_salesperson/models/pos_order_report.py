# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, fields, api
from odoo import tools

class PosOrderReport(models.Model):
    _inherit = 'report.pos.order'
    
    
    sh_salesperson_id = fields.Many2one('res.users', string='Salesperson')

    def _select(self):
        print(f"\n\n\n\t--------------> 15 ")
        query = super()._select()
        return query + """,
            l.sh_salesperson_id AS sh_salesperson_id
        """

    def _group_by(self):
        print(f"\n\n\n\t--------------> 22 ")
        query = super()._group_by()
        return query + """,
            l.sh_salesperson_id
        """
