# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'CRM Custom Field',
    'version': '1.0',
    'summary': 'CRM Custom',
    'sequence': 10,
    'description': """"
CRM Custom
====================

    """,
    'category': 'CRM Custom',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'crm'],

    'data' : [
        # 'security/ir.model.access.csv',
        'views/sh_custom_field_view.xml',
        # 'views/sh_category_view.xml',
        # 'views/sh_member_view.xml',
        # 'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}