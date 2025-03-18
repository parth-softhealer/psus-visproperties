# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Ecommerce Product Question and Answer",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "0.0.1",
    "depends": ["sale_project", "website_sale"],
    "data": [
        "data/mail_templates.xml",
        "security/ir.model.access.csv",
        "views/product_category_view.xml",
        "views/project_task_view.xml",
        "views/sale_order_view.xml",
        "wizard/sale_share_service_form_views.xml",
        "views/sh_wsale_product_question_after_checkout_form.xml",
        "views/website_sale_template.xml",
        "views/sale_order_portal.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "sh_wsale_product_question_after_checkout/static/src/scss/form_style.scss",
        ],
    },
    "images": [
        "static/description/background.png",
    ],
    "live_test_url": "https://youtu.be/QGhyIqkg4W4",
    "installable": True,
    "auto_install": False,
    "application": True,
    'license': 'OPL-1',

}
