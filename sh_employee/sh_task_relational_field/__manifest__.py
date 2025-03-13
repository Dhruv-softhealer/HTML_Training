{
    'name' : 'Task Relational Field',
    'sequence' : 10,
    'summary' : 'Relational field practice',
    'description' : 'Description',
    'depends' : ['base_setup','web'],
    'data':[
        'security/ir.model.access.csv',
        'views/sh_category_view.xml',
        'views/sh_department_view.xml',
        'views/sh_employee_view.xml',
        'views/sh_job_view.xml',
        'views/sh_menuitems.xml'
    ]
}