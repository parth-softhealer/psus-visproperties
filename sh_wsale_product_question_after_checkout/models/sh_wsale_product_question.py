# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleProductQuestion(models.Model):
    _name = "sh.wsale.product.question"
    _rec_name = "title"
    _order = "sequence,id"
    _description = "Sale Product Question"

    title = fields.Char(required=True, translate=True)
    question_type = fields.Selection(
        [
            ("char_box", "Single Line Text Box"),
            ("text_box", "Multiple Lines Text Box"),
            ("simple_choice", "Selection"),
            ("file", "File Input"),
        ],
        default="char_box",
        string="Question Type",
        required=True,
    )
    product_category_id = fields.Many2one(
        "product.category", "Product Category Question", ondelete="cascade"
    )
    answer_ids = fields.One2many(
        "sh.wsale.product.question.answer.choice", "question_id", "Answers", copy=True
    )
    sequence = fields.Integer(default=10)
    is_mandatory_answer = fields.Boolean("Mandatory Answer")
    question_dec = fields.Html("Question Description")
    error_message = fields.Char("Error Message")
