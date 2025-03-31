# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class AutoSaleWorkflow(models.Model):
    _name = 'sh.auto.sale.workflow'
    _description = 'Auto Sale Workflow'
    
    
    name = fields.Char(string="Name")
    val_order = fields.Boolean(string="Delivery Order")
    force_transfer = fields.Boolean(string="Force Transfer")
    create_invoice = fields.Boolean(string="Create Invoice")
    val_invoice  = fields.Boolean(string="Validate Invoice")
    register_payment = fields.Boolean(string="Register Payment")
    send_invoice_by_email = fields.Boolean(string="Send Invoice By Email")
    sh_sale_journal = fields.Many2one('account.journal',string="Sale Journal")
    payment_journal = fields.Many2one('account.journal', string="Payment Journal")
    payment_method = fields.Many2one('account.payment.method.line', string="Payment Method")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
        
    
    @api.onchange('create_invoice' , 'val_invoice' , 'register_payment' )
    def handle_checkbox(self):
       if self.create_invoice==False:
           self.val_invoice = False
           self.payment_journal = None
           self.payment_method = None
           
       if self.val_invoice==False:
           self.register_payment = False
           self.send_invoice_by_email=False
       
       if  self.register_payment==False:
           self.payment_journal= None
           

    
    