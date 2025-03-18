# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _
from odoo.exceptions import AccessError
from odoo.http import request, content_disposition


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def binary_content(
        self,
        xmlid=None,
        model="ir.attachment",
        id=None,
        field="datas",
        unique=False,
        filename=None,
        filename_field="name",
        download=False,
        mimetype=None,
        default_mimetype="application/octet-stream",
        access_token=None,
    ):
        if id and model == "sh.wsale.product.question.answer":
            record = self.env[model].sudo().browse(int(id))
            if not record or not record.exists():
                return (404, [], None) 
                       
            if record and access_token:
                if record.sale_order_line_id.sudo():
                    if (
                        not record.sale_order_line_id.sudo().order_id.sudo().access_token
                        == access_token
                    ):
                        return (404, [], None)

                    status, content, filename, mimetype, filehash = self.env['ir.http']._binary_record_content(
                        record, field=field, filename=None, filename_field=filename_field,
                        default_mimetype='application/octet-stream')
                    status, headers, content = self.env['ir.http']._binary_set_headers(
                        status, content, filename, mimetype, unique, filehash=filehash, download=download)

                    return status, headers, content
    
        return super(Http, self).binary_content(
            xmlid=xmlid,
            model=model,
            id=id,
            field=field,
            unique=unique,
            filename=filename,
            filename_field=filename_field,
            download=download,
            mimetype=mimetype,
            default_mimetype=default_mimetype,
            access_token=access_token,
        )