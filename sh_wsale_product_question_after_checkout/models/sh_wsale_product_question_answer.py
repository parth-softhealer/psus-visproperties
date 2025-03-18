# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _
from odoo.exceptions import UserError


class ProductQuestionAnswer(models.Model):
    _name = "sh.wsale.product.question.answer"
    _description = "Product Question Answer"
    _rec_names_search = ["value_answer_id", "value_text_box"]

    question_id = fields.Many2one(
        "sh.wsale.product.question",
        ondelete="restrict",
        required=True,
    )
    project_task_id = fields.Many2one("project.task", ondelete="cascade")
    sale_order_id = fields.Many2one("sale.order", ondelete="cascade")
    partner_id = fields.Many2one("res.partner", related="project_task_id.partner_id")
    question_type = fields.Selection(related="question_id.question_type")
    value_answer_id = fields.Many2one(
        "sh.wsale.product.question.answer.choice", string="Suggested answer"
    )

    value_text_box = fields.Text("Multiple Line answer")
    value_char_box = fields.Char("Single Line answer")
    value_file = fields.Binary("File answer")

    sale_order_line_id = fields.Many2one("sale.order.line")
