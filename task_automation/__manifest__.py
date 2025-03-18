# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Task Automation',
    'summary': 'Task Automation',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'http://www.confianzit.com',
    'version': '0.0.1',
    'author': 'Confianz Global',
    'depends': ['tour_api_integration', 'calendar', 'project', 'account_accountant'],
    'data': [
        'security/task_automation_security.xml',
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/account_invoice.xml',
        'views/product_template.xml',
        'views/purchase_view.xml',
        'views/res_company_views.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}



