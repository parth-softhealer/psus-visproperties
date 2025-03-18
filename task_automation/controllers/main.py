# Part of odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request, serialize_exception
import requests
import base64

class iGuideController(http.Controller):

    @http.route("/webhook", methods=["POST"], type='json', auth="public", csrf=False)
    def iguide_ready(self):
        try:
            content = request.jsonrequest
            billing_ifo = content.get('billingInfo', {})
            urls = content.get('urls', {})
            pdf_floor_ft = urls.get('media', {}).get('pdfImperial')
            unbranded_url = urls.get('unbrandedUrl')
            full_address = content.get('property', {}).get('fullAddress')
            filename = pdf_floor_ft['en'].split('/')[-1] if pdf_floor_ft else False
            res = requests.get(pdf_floor_ft['en']) if pdf_floor_ft else False
            task = request.env['project.task'].sudo().search([
                ('iguide_client_address', '=', full_address),
                ('stage_id.is_media_uploaded', '=', True),
                ('is_processed', '=', False),
                ('sale_line_id.product_id.categ_id.is_iguide', '=', True)],
                limit=1)
            if task:
                task.sudo().write({
                    'x_studio_storybook_link_1': unbranded_url,
                    'x_studio_floor_plan_pdf_filename': filename if res else False,
                    'x_studio_floor_plan_pdf': base64.b64encode(res.content) if res else False,
                    'x_studio_iguide_billable_sq_ft': billing_ifo.get('billableAreaSqFeet'),
                    'is_processed': True
                })
            return {
                    'code': 200,
                    'message': 'Success' if task else 'Record NotFound',
                    }

        except Exception as e:
            return {
                'code': 500,
                'message': "Odoo Server Error",
                'data': serialize_exception(e)
            }
