# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Book Published Time',
    'sequence': 10,
    'description': """"
Book Published Time
====================

    """,
    'category': 'Book Published Time',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'sale'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_book_published_view.xml',
        # 'views/sh_category_view.xml',
        # 'views/sh_member_view.xml',
        # 'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}