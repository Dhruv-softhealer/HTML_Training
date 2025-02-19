# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Library Management System',
    'sequence': 10,
    'description': """
Library Management
====================

    """,
    'category': 'Library',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_book_view.xml',
        'views/sh_category_view.xml',
        'views/sh_member_view.xml',
        'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}