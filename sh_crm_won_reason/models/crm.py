# -*- coding: utf-8 -*-
# Softhealer Technologies

from odoo import api, fields, models, _

class Crm(models.Model):
    _inherit="crm.lead"

    won_reason_id = fields.Many2one(
        'crm.won.reason', string='Won Reason',
        index=True, ondelete='restrict', tracking=True)
   