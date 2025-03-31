# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from markupsafe import Markup
from odoo import api, fields, models, _
from odoo.tools.mail import is_html_empty


class CrmLeadWon(models.TransientModel):
    _name = 'crm.lead.won'
    _description = 'Get Won Reason'

    lead_ids = fields.Many2many('crm.lead', string='Leads')
    won_reason_id = fields.Many2one('crm.won.reason', 'Won Reason')
    won_feedback = fields.Html(
        'Closing Note', sanitize=True
    )

    def action_won_reason_apply(self):
        """Mark lead as lost and apply the loss reason"""
        self.ensure_one()
        if self.won_feedback:
            self.lead_ids._track_set_log_message(
                Markup('<div style="margin-bottom: 4px;"><p>%s:</p>%s<br /></div>') % (
                    _('Lost Comment'),
                    self.won_feedback
                )
            )
        if self.lead_ids:
            self.lead_ids.write({
                "won_reason_id" :self.won_reason_id.id
            })
        
        res = self.lead_ids.action_set_won()
        return res
