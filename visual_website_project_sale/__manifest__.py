{
    'name': 'Visual Properties: Multiple Dev',
    'summary': 'Visual Properties: Multiple Dev',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '0.0.1',
    'author': 'Odoo Inc',
    'description': """
Visual Properties: Multiple Dev
===============================
*[#2070756]
    - photographer on Sale order to Purchase order
    - project/task created from e-commerce side
    - shipping address consider as a billing address
*[#2211888]
    - Update photographer on Project task to Sale Order and Purchase order
    """,
    'category': 'Custom Development',
    'depends': ['sale', 'sale_management', 'sale_purchase', 'website_sale', 'project', 'sale_timesheet', 'purchase_stock', 'sale_project'],
    # website_sale_delivery remove by softherlaer
    'data': [
        'views/product_views.xml',
        'views/sale_views.xml',
        # 'views/website_sale_template.xml',
        'views/project_views.xml',
        'data/data.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
