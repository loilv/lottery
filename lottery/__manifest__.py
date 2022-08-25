# -*- coding: utf-8 -*-

{
    "name": "Đại lý vé số",
    "description": """""",
    "summary": "",
    "category": "Lottery/Backend",
    "version": "15.0.1.0.1",
    'author': '',
    'company': '',
    'maintainer': '',
    'website': "",
    "depends": ['base', 'web', 'mail'],
    "data": [
        'security/ir.model.access.csv',
        'data/res_group.xml',
        'views/planed.xml',
        'wizard/create_plan.xml',
        'wizard/create_return_stock.xml',
        'wizard/purchase_inventory_wz.xml',
        'wizard/create_customer.xml',
        'views/purchase_inventory.xml',
        'views/customer.xml',
        'views/return_stock_view.xml',
        'data/data_tele_data.xml',
        'data/data_planed.xml',
        'data/province_lottery_data.xml',
        'data/schedule.xml',
        'views/res_users.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'code_backend_theme/static/src/scss/login.scss',
        ],
        'web.assets_backend': [
            'lottery/static/src/js/customer.js',
            'lottery/static/src/js/custom_option_field.js',
        ],
        'web.assets_qweb': [

        ],
    },
    'images': [

    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
