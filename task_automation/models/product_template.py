# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    billed_service_ok = fields.Boolean(string='Billed with Services', copy=False)

class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_iguide = fields.Boolean(string='Is iGuide', copy=False)