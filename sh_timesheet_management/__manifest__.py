# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Timesheet Management',
    'version': '1.0',
    'summary': 'Timesheet Management',
    'sequence': 10,
    'description': """"
Timesheet Management
====================

    """,
    'category': 'Timesheet Management',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'sale', 'mail'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_tag_view.xml',
        'views/sh_task_view.xml',
        'views/sh_timesheet_view.xml',
        'views/sh_menuitems_view.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}