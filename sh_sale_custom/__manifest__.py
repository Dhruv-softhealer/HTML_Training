# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Custom Sale Management',
    'version': '1.0',
    'summary': 'Sale Custom',
    'sequence': 10,
    'description': """"
Sale Custom
====================

    """,
    'category': 'Sale Custom',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'sale'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_note_view.xml',
        # 'views/sh_category_view.xml',
        # 'views/sh_member_view.xml',
        # 'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}