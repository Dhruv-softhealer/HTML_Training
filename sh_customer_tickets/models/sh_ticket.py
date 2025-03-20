# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api, _
from datetime import timedelta

from odoo.exceptions import ValidationError


class Tickets(models.Model):
    _name = 'support.ticket'
    _inherit = ['mail.activity.mixin', 'mail.thread']
    _description = 'Ticket Management'

    name = fields.Char(string="Name", required=True, readonly=True, default=lambda self: _('New'))
    user_id = fields.Many2one(comodel_name='res.users')
    customer_id = fields.Many2one('res.partner', string="Ticket", required=True)
    dev_id = fields.Many2one('res.users', string='Developer', default=lambda self : self.env.uid)
    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Medium'),
         ('2', 'High'),
         ('3', 'Urgent')],
        default='1',
        string="Priority")
    state = fields.Selection(
        [('new', 'New'),
         ('in_progress', 'In Progress'),
         ('resolved', 'Resolved'),
         ('closed', 'Closed'),
         ('cancel', 'Cancel')],
        # default='new',
        string="State"
    )
    date_begin = fields.Datetime(default=fields.Datetime.now())
    date_end = fields.Datetime()
    invoice_ids = fields.One2many('account.move', 'ticket_id', string="InvoiceIDs")
    
    
    # ================================= DEFAULT GET METHOD ==================================
    
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['priority'] = '1' # Default priority is 'Medium'
        res['state'] = 'new' # Default Status is 'New'
        return res
    
    
    # ================================= SEQUENCE ==================================
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', ("New")) == ("New"):
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals['create_date'])
                ) if 'create_date' in vals else None
                vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
                    'support.ticket', sequence_date=seq_date) or _("New")

        return super().create(vals_list)
    
    
    # ================================= WRITE STATE =================================
    
    def write(self, vals):
        if 'state' in vals:
            for ticket in self: 
                old_state = ticket.state
                new_state = vals.get('state')
                message = f'Status Changed from "{old_state}" to "{new_state}"'
                print("\n\n\n\n::::::::",message,":::::::::\n\n\n\n")
                
            if vals['state'] == 'closed':
                ticket_invoice = self.env['account.move'].create([{
                    'partner_id':self.customer_id.id,
                    'move_type':'out_invoice',
                    'ticket_id' : self.id,
                    'invoice_date':fields.Date.today(),
                    'invoice_line_ids':[(0,0,{
                        'name':f'SH Ticket {self.name}',
                        'quantity' : 1,
                        'price_unit' : 10
                    })]
                }])
                ticket_invoice.state = 'posted' 
                
        return super().write(vals)
    
    
    # ================================= SMART BUTTON ==================================
    
    def get_invoices(self):
        if len(self.invoice_ids) > 1:
            return {
                'type':'ir.actions.act_window',
                'view_mode':'list,form',
                'res_model':'account.move',
                'domain':[('ticket_id', '=', self.id)]
            }
        return {
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'account.move',
            'res_id':self.invoice_ids.id
        }
        
        
    # ================================= WIZARD ==================================
 
    def action_to_open_wizard(self):
        return{
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'ticket.update.wizard',
            'target' : 'new',
            'context':{'hi':'hi'}
        }
        
        
        # ================================= CHANGE STATE ==================================
        
    def set_ticket_to_start(self):
        self.state = 'in_progress'
        
    def set_ticket_to_resolved(self):
        self.state = 'resolved'
        
    def set_ticket_to_closed(self):
        self.state = 'closed'
    
    def set_ticket_to_cancel(self):
        self.state = 'cancel'
        
        
    # ================================= CRONE JOB ==================================
        
    def auto_close_resolved_tickets(self):
        limit_date = fields.Datetime.now()
        tickets = self.search([
            ('state', '=', 'resolved'),
            ('write_date', '<', limit_date)
        ])
        tickets.write({'state': 'closed'})
        
        
    # ================================= API CONSTRAIN ==================================
        
    @api.constrains('dev_id')
    def _check_dev_id(self):
        for record in self:
            existing_ticket = self.search([
                ('dev_id', '=', record.dev_id.id),
                ('state', 'not in', ['closed', 'cancel']),
                ('id', '!=', record.id) 
            ])
            print(existing_ticket,self)
            if existing_ticket:
                raise ValidationError(f"{record.dev_id.name} already has an active ticket! Close or cancel it before assigning a new one.")
        
        
        
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
   
        
    
        
    
class TicketUpdatedWizard(models.TransientModel):
    _name = 'ticket.update.wizard'
    _description = 'Ticket Wizard'
    
    status = fields.Selection(
        [('new', 'New'),
         ('in_progress', 'In Progress'),
         ('resolved', 'Resolved'),
         ('closed', 'Closed'),
         ('cancel', 'Cancel')],
        required=True
    )
    def update_ticket_status(self):
        print(self.env.context)
        active_ids = self.env.context.get('active_ids')
        res = self.env['support.ticket'].browse(active_ids)
        res.write({'state':self.status})