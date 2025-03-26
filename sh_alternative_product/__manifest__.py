# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name': 'Product Management',
    'version': '1.0',
    'summary': 'Product Management',
    'sequence': 10,
    'description': """"
Product Management
====================

    """,
    'category': 'Product Management',
    'website': 'https://softhealer.com',

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base_setup','sale'],

    'data': [
        'security/sh_alt_product_group.xml',
        'security/ir.model.access.csv',
        'views/sh_product_varient_view.xml',
        'views/sh_sale_wizard_btn.xml',
        'views/sh_replace_wizard_form.xml'
    ],
    
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
    
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/sh_demo_data.xml',
    # ],
}

