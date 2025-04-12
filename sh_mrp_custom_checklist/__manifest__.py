# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Manufacturing Checklist',
    'version': '1.0',
    'summary': 'Manufacturing Checklist',
    'sequence': 1,
    'description': """"
Manufacturing Checklist
====================

    """,
    'category': 'Manufacturing Checklist',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web', 'mrp'],

    'data': [
        'security/sh_mrp_checklist_access.xml',
        'security/ir.model.access.csv',
        'report/sh_custom_checklist_report.xml',
        'views/sh_mrp_custom_checklist.xml',
        'views/sh_mrp_checklist_template.xml',
        'views/sh_mrp_checklist_page.xml',
        'views/sh_mrp_import_checklist.xml',
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

