# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Auto Sale Workflow',
    'version': '1.0',
    'summary': 'Auto Sale Workflow',
    'sequence': 1,
    'description': """"
Auto Sale Workflow
====================

    """,
    'category': 'Auto Sale Workflow',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web','account','sale', 'crm'],

    'data': [
        'security/sh_security_group.xml',
        'security/ir.model.access.csv',
        'views/sh_auto_sale_workflow.xml',
        'views/sh_sale_config_fields.xml',
        'views/sh_auto_sale_field.xml',
        'views/sh_menuitem.xml',
    ],
    
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
    
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/sh_demo_data.xml',
    # ],
}

