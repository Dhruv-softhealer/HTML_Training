# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Employee Management',
    'version': '1.0',
    'summary': 'Employee',
    'sequence': 10,
    'description': """
Employee Management
====================

    """,
    'category': 'Employee',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_emp_view.xml',
        'views/sh_department_view.xml',
        'views/sh_job_view.xml',
        'views/sh_category_view.xml',
        'views/sh_menuitems.xml'
        
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}
