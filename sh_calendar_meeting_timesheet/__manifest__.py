# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Calendar Meeting Timesheet',
    'version': '1.0',
    'summary': 'Calendar Meeting Timesheet',
    'sequence': 1,
    'description': """"
Calendar Meeting Timesheet
====================

    """,
    'category': 'Calendar Meeting Timesheet',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web','account', 'calendar'],

    'data': [
        # 'demo/sh_demo.xml',
        'security/sh_calendar_timesheet_access.xml',
        'security/ir.model.access.csv',
        'views/sh_calendar_timesheet.xml',
        'views/sh_timesheet_setting.xml',
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

