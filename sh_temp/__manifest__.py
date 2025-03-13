# -*- coding: utf-8 -*-
# Part of Softhealer Technologies
{
    'name' : 'Temp',
    'version' : '1.0',
    'sequence': 10,
    'summary' : 'Employee Management',
    'category' : 'Employees',
    'description' : '''
Employee
====================
Employee Management Application
''',
    'website':'https://www.softhealer.com/',
    'depends' : ['base_setup','web'],

    'data' : [
        'security/ir.model.access.csv',
        'views/employee_views.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3'
}