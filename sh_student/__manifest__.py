# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Student Management',
    'version': '1.0',
    'summary': 'Student Management System',
    'sequence': 10,
    'description': """
Student Management
====================

    """,
    'category': 'Student',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web'],

    'data' : [
        'views/sh_students_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}