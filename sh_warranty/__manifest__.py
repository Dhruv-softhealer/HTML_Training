# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Warranty Sale Management',
    'version': '1.0',
    'summary': 'Sale Warranty',
    'sequence': 10,
    'description': """"
Sale Warranty
====================

    """,
    'category': 'Sale warranty',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'sale'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_sale_warranty_view.xml',
        'reports/sh_report_view.xml',
        # 'views/sh_member_view.xml',
        # 'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}