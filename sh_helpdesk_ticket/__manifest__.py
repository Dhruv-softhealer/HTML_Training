# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Helpdesk Ticket',
    'version': '1.0',
    'summary': 'Helpdesk Ticket',
    'sequence': 1,
    'description': """"
Helpdesk Ticket
====================

    """,
    'category': 'Helpdesk Ticket',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web','account', 'calendar'],

    'data': [
        'security/sh_helpdesk_ticket_access.xml',
        'security/ir.model.access.csv',
        'views/sh_helpdesk_setting.xml',
        'views/sh_create_helpdesk_task.xml',
    ],
    
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
    
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/sh_demo.xml',
    # ]
    # ,
}

