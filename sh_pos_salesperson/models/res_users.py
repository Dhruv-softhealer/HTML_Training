# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.


from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'
    

    @api.model
    def _load_pos_data_domain(self, data):
        return []
