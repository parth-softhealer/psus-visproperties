# -*- coding: utf-8 -*-
{
    'name': 'Sh_hide_extra_address',
    'version': '1.0.0',
    'summary': """ Sh_hide_extra_address Summary """,
    'author': '',
    'website': '',
    'category': '',
    'depends': ['base', 'web','website_sale'],
    'data': [
        "views/templates.xml"
    ],
    'assets': {
              'web.assets_backend': [
                  'sh_hide_extra_address/static/src/**/*'
              ],
          },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
