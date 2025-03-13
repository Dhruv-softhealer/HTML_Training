# -*- coding: utf-8 -*-
# Part of Softhealer Technologies
{
    'name' : 'Master Button',
    'version' : '1.0',
    'sequence': 10,
    'summary' : 'Master Button',
    'category' : 'Employees',
    'description' : '''
Employee
====================
Master Button Creation
''',
    'website':'https://www.softhealer.com/',
    'depends' : ['base_setup','web','sale','product'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_sale_order_products_views.xml',
        'views/sh_customer_orders_views.xml',
        'views/sh_employee_form_download_views.xml',
        'views/sh_menuitems.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3'
}