from odoo import models


class Customer(models.Model):
    _inherit = ['res.partner']


    # ================================= SMART BUTTON ==================================

    def action_get_tickets(self):
        return{
            'type':'ir.actions.act_window',
            'view_mode':'list',
            'res_model':'support.ticket',
            'domain':[('customer_id','=',self.id)]
        }