# -*- coding: utf-8 -*-
# Part of Softhealer Technologies
 
from odoo import models,api,fields
from odoo.exceptions import UserError
 
class AnalyticEvent(models.Model):
    _inherit = 'account.analytic.line'
 
    
    @api.constrains('date')
    def _restrict_backdate(self):
        for rec in self:
            days_limit = (fields.Date.today() - rec.date).days > rec.company_id.backdate_days_limit
            if days_limit:
                if not self.env.user.has_group('sh_timesheet_backdate_registration.sh_timesheet_backdate_access_group'):
                    raise UserError(f'You are not allow to fill timesheet before {rec.company_id.backdate_days_limit} day(s)')