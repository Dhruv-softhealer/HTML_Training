# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields

class TicketInvoice(models.Model):
    _inherit = 'account.move'
    
    ticket_id = fields.Many2one('support.ticket')