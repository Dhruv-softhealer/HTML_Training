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
        'security/ir.model.access.csv',
        'views/sh_student_view.xml',
        'views/sh_class_view.xml',
        'views/sh_teacher_view.xml',
        'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}