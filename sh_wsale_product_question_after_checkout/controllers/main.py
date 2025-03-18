# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.http import request
import base64
from werkzeug.exceptions import NotFound


class PRoductQuestionCheckout(http.Controller):

    @http.route(
        "/sh_wsale_product_question_after_checkout",
        type="http",
        auth="public",
        methods=["GET", "POST"],
        website=True,
    )
    def sh_wsale_product_question_after_checkout_website_form(self, **kwargs):

        error = dict()
        value = dict()
        sale_order_id = http.request.params.get("sale_order_id")
        access_token = http.request.params.get("access_token")
        sale_order_obj = (
            request.env["sale.order"]
            .sudo()
            .search(
                [
                    ("id", "=", sale_order_id),
                    ("access_token", "=", access_token),
                ],
                limit=1,
            )
        )
        if sale_order_obj:
            sale_order_obj = sale_order_obj.sudo()
        else:
            raise NotFound()

        # get method code
        if request.httprequest.method == "GET":

            if (
                sale_order_obj
                and sale_order_obj.order_line
                and sale_order_obj.order_line.product_id
            ):
                save_value = {}
                value = {
                    "error": error,
                    "sale_order_obj": sale_order_obj,
                    "access_token": access_token,
                    "order_line": sale_order_obj.order_line,
                    "save_value": save_value,
                }

                # once ans is created.
                if (
                    sale_order_obj.sh_wsale_product_question_after_checkout_sh_question_answer_ids
                ):

                    ans_obj = (
                        sale_order_obj.sh_wsale_product_question_after_checkout_sh_question_answer_ids.sudo()
                    )
                    for ans in ans_obj:

                        if ans.question_type == "char_box":
                            save_value[
                                "%s_%s"
                                % (
                                    ans.sale_order_line_id.sudo().id,
                                    ans.question_id.sudo().id,
                                )
                            ] = ans.value_char_box
                        if ans.question_type == "text_box":
                            save_value[
                                "%s_%s"
                                % (
                                    ans.sale_order_line_id.sudo().id,
                                    ans.question_id.sudo().id,
                                )
                            ] = ans.value_text_box

                        if ans.question_type == "simple_choice":
                            save_value[
                                "%s_%s"
                                % (
                                    ans.sale_order_line_id.sudo().id,
                                    ans.question_id.sudo().id,
                                )
                            ] = ans.value_answer_id.sudo().id
                        if ans.question_type == "file":
                            save_value[
                                "%s_%s"
                                % (
                                    ans.sale_order_line_id.sudo().id,
                                    ans.question_id.sudo().id,
                                )
                            ] = ans.id

                    value["save_value"] = save_value
                return request.render(
                    "sh_wsale_product_question_after_checkout.qustion_request_form",
                    value,
                )

        # post method in the form
        if request.httprequest.method == "POST":
            save_value = kwargs

            question_number = list(kwargs.keys())
            question_number.remove("sale_order_id")
            question_number.remove("access_token")
            question_list = []
            new_question_list = []
            for line in sale_order_obj.order_line:

                for (
                    qus
                ) in (
                    line.product_id.categ_id.sh_wsale_product_question_after_checkout_sh_question_ids
                ):

                    if qus.is_mandatory_answer:

                        new_question_list.append("%s_%s" % (line.id, qus.id))
            for item in new_question_list:

                if item in question_number:

                    if not kwargs[item]:
                        error[item] = "error"

                else:

                    error[item] = "error"

            value = {
                "save_value": save_value,
                "sale_order_obj": sale_order_obj,
                "access_token": sale_order_obj.access_token,
                "order_line": sale_order_obj.order_line,
                "error": error,
            }

            for val in question_number:

                find_ = val.find("_")
                if find_ != -1:
                    question_id = val[find_ + 1 :]
                    question_list.append(question_id)

            question_obj = (
                request.env["sh.wsale.product.question"]
                .sudo()
                .search([("id", "in", question_list)])
            )

            if not value["error"]:

                if question_obj:
                    question_obj.sudo()

                if question_obj:
                    ans_dic = {}

                    if (
                        sale_order_obj.sh_wsale_product_question_after_checkout_sh_question_answer_ids
                    ):
                        for line in sale_order_obj.order_line:
                            for (
                                ans
                            ) in (
                                sale_order_obj.sh_wsale_product_question_after_checkout_sh_question_answer_ids.sudo()
                            ):

                                ans_ids_list = (
                                    sale_order_obj.sh_wsale_product_question_after_checkout_sh_question_answer_ids.sudo()
                                    .filtered(
                                        lambda l: l.sale_order_line_id.id == line.id
                                    )
                                    .question_id.ids
                                )
                                for question in question_obj:
                                    ans_dic = {
                                        "sale_order_id": sale_order_obj.id,
                                        "question_id": question.id,
                                        "question_type": question.question_type,
                                        "partner_id": sale_order_obj.partner_id,
                                        "sale_order_line_id": line.id,
                                    }
                                    if line.task_id:
                                        ans_dic["project_task_id"] = line.task_id.id
                                    if ans.sale_order_line_id.id == line.id:
                                        if question.id in ans_ids_list:
                                            if question.id == ans.question_id.id:
                                                if ans.question_type == "simple_choice":
                                                    ans.value_answer_id = kwargs[
                                                        "%s_%s" % (line.id, question.id)
                                                    ]
                                                if ans.question_type == "text_box":
                                                    ans.value_text_box = kwargs[
                                                        "%s_%s" % (line.id, question.id)
                                                    ]
                                                if ans.question_type == "char_box":
                                                    ans.value_char_box = kwargs[
                                                        "%s_%s" % (line.id, question.id)
                                                    ]
                                                if ans.question_type == "file":
                                                    if kwargs[
                                                        "%s_%s" % (line.id, question.id)
                                                    ]:

                                                        file = kwargs[
                                                            "%s_%s"
                                                            % (line.id, question.id)
                                                        ]
                                                        attachment = file.read()
                                                        ans.value_file = (
                                                            base64.b64encode(attachment)
                                                        )
                                        else:
                                            if (
                                                question.question_type
                                                == "simple_choice"
                                            ):
                                                ans_dic["value_answer_id"] = kwargs[
                                                    "%s_%s" % (line.id, question.id)
                                                ]
                                                if ans_dic["value_answer_id"]:
                                                    request.env[
                                                        "sh.wsale.product.question.answer"
                                                    ].sudo().create(ans_dic)
                                            if question.question_type == "text_box":
                                                ans_dic["value_text_box"] = kwargs[
                                                    "%s_%s" % (line.id, question.id)
                                                ]

                                                if ans_dic["value_text_box"]:
                                                    request.env[
                                                        "sh.wsale.product.question.answer"
                                                    ].sudo().create(ans_dic)
                                            if question.question_type == "char_box":
                                                ans_dic["value_char_box"] = kwargs[
                                                    "%s_%s" % (line.id, question.id)
                                                ]
                                                if ans_dic["value_char_box"]:
                                                    request.env[
                                                        "sh.wsale.product.question.answer"
                                                    ].sudo().create(ans_dic)
                                            if question.question_type == "file":
                                                file = kwargs[
                                                    "%s_%s" % (line.id, question.id)
                                                ]
                                                attachment = file.read()
                                                ans_dic["value_file"] = (
                                                    base64.b64encode(attachment)
                                                )
                                                if ans_dic["value_file"]:
                                                    request.env[
                                                        "sh.wsale.product.question.answer"
                                                    ].sudo().create(ans_dic)

                            value["success"] = "success"
                    else:

                        for line in sale_order_obj.order_line:

                            for question in question_obj:

                                ans_dic = {
                                    "sale_order_id": sale_order_obj.id,
                                    "question_id": question.id,
                                    "question_type": question.question_type,
                                    "partner_id": sale_order_obj.partner_id,
                                    "sale_order_line_id": line.id,
                                }
                                if line.task_id:
                                    ans_dic["project_task_id"] = line.task_id.id

                                if "%s_%s" % (line.id, question.id) in question_number:

                                    if question.question_type == "simple_choice":

                                        ans_dic["value_answer_id"] = kwargs[
                                            "%s_%s" % (line.id, question.id)
                                        ]
                                        if ans_dic["value_answer_id"]:
                                            request.env[
                                                "sh.wsale.product.question.answer"
                                            ].sudo().create(ans_dic)
                                    if question.question_type == "text_box":
                                        ans_dic["value_text_box"] = kwargs[
                                            "%s_%s" % (line.id, question.id)
                                        ]

                                        if ans_dic["value_text_box"]:
                                            request.env[
                                                "sh.wsale.product.question.answer"
                                            ].sudo().create(ans_dic)
                                    if question.question_type == "char_box":
                                        ans_dic["value_char_box"] = kwargs[
                                            "%s_%s" % (line.id, question.id)
                                        ]
                                        if ans_dic["value_char_box"]:
                                            request.env[
                                                "sh.wsale.product.question.answer"
                                            ].sudo().create(ans_dic)
                                    if question.question_type == "file":
                                        file = kwargs["%s_%s" % (line.id, question.id)]
                                        attachment = file.read()
                                        ans_dic["value_file"] = base64.b64encode(
                                            attachment
                                        )
                                        if ans_dic["value_file"]:
                                            request.env[
                                                "sh.wsale.product.question.answer"
                                            ].sudo().create(ans_dic)

                                    value["success"] = "success"

            if value.get("success") and not value["error"]:
                return request.render(
                    "website.contactus_thanks",
                )
            return request.render(
                "sh_wsale_product_question_after_checkout.qustion_request_form",
                value,
            )
