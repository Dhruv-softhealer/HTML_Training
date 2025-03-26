from odoo import fields, models


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
        if res.state == 'closed':
            res.set_ticket_to_closed()