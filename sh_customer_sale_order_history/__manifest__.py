# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Customer Sale Order History',
    'version': '1.0',
    'summary': 'Customer Sale Order History',
    'sequence': 1,
    'description': """"
Customer Sale Order History
====================

    """,
    'category': 'Customer Sale Order History',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','web','account','sale','sale_management', 'crm'],

    'data': [
        # 'demo/sh_demo.xml',
        'security/sh_order_history_access.xml',
        'security/ir.model.access.csv',
        'views/sh_sale_setting_fields.xml',
        'views/sh_order_history.xml',
        # 'views/sh_auto_sale_field.xml',
        # 'views/sh_menuitem.xml',
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

