# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Tickets Management',
    'version': '1.0',
    'summary': 'Tickets Management',
    'sequence': 10,
    'description': """"
Tickets Management
====================

    """,
    'category': 'Tickets Management',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base_setup','web', 'mail', 'account'],

    'data': [
        'security/ticket_access_group.xml',
        'security/ticket_record_rules.xml',
        'security/ir.model.access.csv',
        'views/ticket_crone_job.xml',
        'views/sh_ticket_view.xml',
        'views/sh_sequence_view.xml',
        'views/sh_menuitems.xml',
    ],
    
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
    
    # only loaded in demonstration mode
    'demo': [
        'demo/sh_demo_data.xml',
    ],
}

