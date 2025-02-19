# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class Member(models.Model):
    _name = 'sh.member'
    _description = 'Member Details'
    
    name = fields.Char("Member Name")
    contact = fields.Integer("Contact Number")
    email = fields.Char("Email")
    membership_type = fields.Selection([('regular', 'Regular'), ('premium', 'Premium')], string="Type of Membership", compute="_membership_type")
    bk_ids = fields.Many2many("sh.book", relation="sh_library_member_book", string="Books")
    
    @api.depends('bk_ids')
    def _membership_type(self):
        for rec in self:
            if len(rec.bk_ids) < 3:
                rec.membership_type = 'regular'
            else:
                rec.membership_type = 'premium'