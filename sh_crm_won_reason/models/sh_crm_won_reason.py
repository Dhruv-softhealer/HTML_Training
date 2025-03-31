# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ShCrmWonReason(models.Model):
    _name = "crm.won.reason"
    _description = 'Opp. Won Reason'

    name = fields.Char('Description', required=True, translate=True)
    active = fields.Boolean('Active', default=True)