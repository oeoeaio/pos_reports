# -*- coding: utf-8 -*-
{
    'name': 'POS Reports',
    'version': '1.0.0',
    'category': 'Point Of Sale',
    'author': 'Rob Harrington',
    'sequence': 10,
    'summary': 'Adds additional reports for POS orders',
    'description': "",
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_monthly_gst_report_view.xml',
        'views/pos_monthly_payments_report_view.xml',
        'security/ir.model.access.csv',
     ],
    'assets': {},
    'images': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3'
}
