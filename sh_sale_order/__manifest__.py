# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Sale Order Management',
    'version': '1.0',
    'summary': 'Sale Order Management System',
    'sequence': 10,
    'description': """
Sale Order Management
====================

    """,
    'category': 'Sale Order',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_res_partner_view.xml',
        'views/sh_product_view.xml',
        'views/sh_account_tax_view.xml',
        'views/sh_sale_order_view.xml',
        'views/sh_sale_order_line_view.xml',
        'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}