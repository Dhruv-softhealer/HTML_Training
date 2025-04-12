# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Timesheet Backdate Registration',
    'version': '1.0',
    'summary': 'Timesheet Backdate Registration',
    'sequence': 1,
    'description': """"
Timesheet Backdate Registration
====================

    """,
    'category': 'Timesheet Backdate Registration',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web', 'project', 'account' ,'calendar'],

    'data': [
        'security/sh_timesheet_backdate_access.xml',
        'security/ir.model.access.csv',
        'views/sh_backdate_timesheet_view.xml',
        # 'views/sh_create_helpdesk_task.xml',
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

