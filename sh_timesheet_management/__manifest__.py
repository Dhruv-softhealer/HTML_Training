# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'Timesheet Management',
    'version': '1.0',
    'summary': 'Timesheet Management',
    'sequence': 10,
    'description': """"
Timesheet Management
====================

    """,
    'category': 'Timesheet Management',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'sale', 'mail', 'crm'],
# for chatter add mail option in depends.
    'data' : [
        'security/timesheet_access.xml',
        'security/ir.model.access.csv',
        'reports/sh_quotation_report_view.xml',
        # 'static/src/SCSS/sh_course_pdf_report.scss',
        # 'static/src/SCSS/sh_course_report.scss',
        'views/sh_tag_view.xml',
        'views/sh_task_view.xml',
        'views/sh_timesheet_view.xml',
        'views/sh_menuitems_view.xml',
    ],
    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}