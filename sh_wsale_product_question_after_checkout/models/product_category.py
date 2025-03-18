# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api,models,fields, _

class ProductCategory(models.Model):

    _inherit = 'product.category'

    sh_wsale_product_question_after_checkout_sh_question_ids = fields.One2many(
        'sh.wsale.product.question','product_category_id',
        string='Questions', copy=True)