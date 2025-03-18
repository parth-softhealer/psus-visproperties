# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import uuid
from odoo import api, models, fields, _

class SaleShare(models.TransientModel):

    _name = 'sh.wsale.product.question.after.checkout.wizard'
    _description = 'Sale Sharing'

    # Default_get Method 
    @api.model
    def default_get(self, fields):
        result = super(SaleShare, self).default_get(fields)

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        context =self.env.context.copy()

        id = context.get('default_order_id')
        order_id = self.env['sale.order'].sudo().browse(context.get('default_order_id',False))

        url = base_url + '/sh_wsale_product_question_after_checkout'+'?'+'sale_order_id='+str(id)+'&access_token='+order_id.access_token

        result['share_link'] = url
        return result

    partner_ids = fields.Many2many('res.partner', string="Recipients", required=True)
    note = fields.Text(help="Add extra content to display in the email")
    share_link = fields.Char(string="Link")
    order_id = fields.Many2one('sale.order')


    # Mail Send Method 
    def sh_action_sale_send_mail(self):
        self.ensure_one()

        sh_sale_service_template_id = self.env.ref('sh_wsale_product_question_after_checkout.sh_sale_service_email_template')

        self.order_id.message_post_with_view(sh_sale_service_template_id,
            values={'note':self.note,'share_link':self.share_link},
            subject=_("You are invited to access %s",self.order_id.name))



