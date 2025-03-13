# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

{
    'name' : 'Sale Custom',
    'version' : '1.0',
    'sequence' : 1,
    'summary' : 'Sale Custom',
    'description' : 'Sale Custom Description',
    'depends' : ['base_setup','web','sale'],
    'data' : [
        'security/ir.model.access.csv',
        'views/sh_views.xml'
    ],
    'installable':True,
    'application':True,
    'license' : 'LGPL-3'
}