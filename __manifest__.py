# -*- coding: utf-8 -*-
{
    'name': "Sparkit BHC",

    'summary': """
        Sparkit BHC""",

    'description': """
        Sparkit BHC
    """,

    'author': "BHC",
    'website': 'www.bhc.be',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sparkit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/community_update_views.xml',
        'views/vrf_views.xml',
        'views/ussd_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'active': True,
}