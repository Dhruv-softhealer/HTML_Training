# -*- coding: utf-8 -*-
# Part of Softhealer Technology.
{
    'name': 'POS Salesperson',
    'version': '1.0',
    'summary': 'POS Salesperson Management',
    'author': 'Softhealer Technologies',
    'company': 'Softhealer Technologies',
    'sequence': 10,
    'description': """
POS Salesperson Management
====================

    """,
    'category': 'Student',
    'website': 'https://softhealer.com',
    'depends': ['base_setup','web', 'point_of_sale','sale'],

    'data' : [
        # 'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/pos_order_line_views.xml',
        'views/pos_order_views.xml',
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            "sh_pos_salesperson/static/src/app/control_buttons/control_buttons.js",
            "sh_pos_salesperson/static/src/app/control_buttons/control_button_views.xml",
            "sh_pos_salesperson/static/src/app/control_buttons/salesperson_views.xml",
            'sh_pos_salesperson/static/src/extend_data.js',
            'sh_pos_salesperson/static/src/salesperson_popup.js',
            'sh_pos_salesperson/static/src/overrides/orderline.xml',
            "sh_pos_salesperson/static/src/overrides/orderline.js"
        ],
    },

    'installable': True,
    'application': True,
    
    'license': 'LGPL-3',
}