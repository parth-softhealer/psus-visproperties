# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    sh_wsale_product_question_after_checkout_sh_question_answer_ids = fields.One2many(
        'sh.wsale.product.question.answer', 'sale_order_id', string='Product Answers')

    @api.model
    def action_sale_share(self):
        self.ensure_one()
        
        context =self.env.context.copy()

        partner_id =[self.partner_id.id]

        context.update({'default_partner_ids':partner_id,'default_order_id':self.id}   )

        action ={
            'type': 'ir.actions.act_window',
            'name': _("Sale Share Service Form"),
            'res_model':'sh.wsale.product.question.after.checkout.wizard',
            'view_type':'form',
            'view_mode':'form',
            'target':'new',
            'context': context,
        }
        return action
            

    def _message_auto_subscribe_notify(self, partner_ids,template):
        """ Notify newly subscribed followers of the last posted message.
            :param partner_ids : the list of partner to add as needaction partner of the last message
                                 (This excludes the current partner)
        """
        return super(SaleOrder, self.with_context(mail_auto_subscribe_no_notify=True))._message_auto_subscribe_notify(partner_ids,template)