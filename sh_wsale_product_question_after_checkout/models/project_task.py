# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _


class ProductTask(models.Model):

    _inherit = "project.task"

    sh_wsale_product_question_after_checkout_sh_question_answer_ids = fields.One2many(
        "sh.wsale.product.question.answer", "project_task_id", string="Product Answers"
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)

        for rec in res:

            if rec.sale_line_id:
                if rec.sale_line_id.order_id:
                    if (
                        rec.sale_line_id.order_id.sh_wsale_product_question_after_checkout_sh_question_answer_ids
                    ):
                        ans_obj = rec.sale_line_id.order_id.sh_wsale_product_question_after_checkout_sh_question_answer_ids.filtered(
                            lambda line: line.sale_order_line_id == rec.sale_line_id
                        )
                        if ans_obj:
                            rec.sh_wsale_product_question_after_checkout_sh_question_answer_ids = (
                                ans_obj.ids
                            )

        return res
