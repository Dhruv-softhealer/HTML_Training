# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Hospital Management',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'sequence': 10,
    'description': """
Hospital Management
====================

    """,
    'category': 'Hospital',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web'],

    'data' : [
        'security/ir.model.access.csv',
        'views/sh_doctor_view.xml',
        'views/sh_patient_view.xml',
        'views/sh_diagnosis_view.xml',
        'views/sh_menuitems.xml'
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}