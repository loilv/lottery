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
    "depends": ['base'],
    "data": [
        'security/ir.model.access.csv',
        'views/planed.xml',
        'wizard/create_plan.xml',
        'wizard/create_return_stock.xml',
        'views/res_users.xml',
        'wizard/purchase_inventory_wz.xml',
        'wizard/create_customer.xml',
        'views/purchase_inventory.xml',
        'views/customer.xml',
        'views/return_stock_view.xml',
        'data/province_lottery_data.xml',
        'data/data_tele_data.xml',
        'data/data_planed.xml',
        'data/schedule.xml',
    ],
    'assets': {
        'web.assets_backend': {

        },
        'web.assets_frontend': {

        },
        'web.assets_qweb': {

        },
    },
    'images': [

    ],
    'license': 'LGPL-3',
    # 'pre_init_hook': 'test_pre_init_hook',
    # 'post_init_hook': 'test_post_init_hook',
    'installable': True,
    'application': True,
    'auto_install': True,
}
