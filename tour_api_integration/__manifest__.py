# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Tour Api Integration',
    'summary': 'Tour Api Integration',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'http://www.confianzit.com',
    'version': '0.0.1',
    'author': 'Confianz Global',
    'depends': ['visual_website_project_sale', 'auth_signup'],
    'data': [
        'views/project_task_views.xml',
	    'views/res_partner_views.xml',
	    'views/res_company_views.xml',
        'views/product_views.xml',
        'data/project_mail_template_data.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}



