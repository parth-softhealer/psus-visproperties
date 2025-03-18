# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_TASK_STATE = [
    ('new_order', 'New Order'),
    ('tour_completed', 'Tour Completed'),
    ('scheduled', 'Scheduled')]


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    #    is_tour_completed = fields.Boolean(string="Is tour complete")
    #    is_new_order = 	fields.Boolean(string="Is new order")
    #    is_scheduled = fields.Boolean(string="Is scheduled")
    state = fields.Selection(_TASK_STATE, 'State')




class ProjectTask(models.Model):
    _inherit = 'project.task'

    x_studio_google_maps = fields.Char(string='Google Maps', compute='_compute_address_url')
    x_state = fields.Selection(
        related='stage_id.state', store=True, readonly=True)
    invoice_id = fields.Many2one('account.move', string='Vendor Bill')
    x_studio_field_KRr2Q = fields.Many2one('calendar.event', state='manual')
    start_datetime = fields.Datetime(related='x_studio_field_KRr2Q.start', string='Shoot Date', store=True)
    iguide_client_address = fields.Char(compute="_compute_iguide_address", readonly=True, store=True, string="iGuide Full Address")
    is_processed = fields.Boolean('IGuide Process Status')
    # comment by softhealer
    x_studio_property_address = fields.Char(related="sale_line_id.order_id.x_studio_property_address_1", string="Property address")
    x_studio_address = fields.Char(related="sale_line_id.order_id.partner_shipping_id.street", string="Address")
    x_studio_address_2 = fields.Char(related="sale_line_id.order_id.partner_shipping_id.street2", string="Address2")
    x_studio_city = fields.Char(related="sale_line_id.order_id.partner_shipping_id.city", string="City")
    x_studio_zip_code = fields.Char(related="sale_line_id.order_id.partner_shipping_id.state_id.code", string="State")
    x_studio_field_O5d3J = fields.Char(related="sale_line_id.order_id.partner_shipping_id.zip", string="Zip Code")


    @api.depends(
        'sale_line_id.order_id.partner_shipping_id',
        'sale_line_id.order_id.partner_shipping_id.street',
        'sale_line_id.order_id.partner_shipping_id.city',
        'sale_line_id.order_id.partner_shipping_id.state_id',
        'sale_line_id.order_id.partner_shipping_id.zip')
    def _compute_iguide_address(self):
        for task in self:
            rec = task.sale_order_id.partner_shipping_id
            if all([rec.street, rec.city, rec.state_id and rec.state_id.code, rec.zip]):
                task.iguide_client_address = rec.street + ' ' + rec.city + ' ' + rec.state_id.code + ' ' + rec.zip

    # Google url
    @api.depends('x_studio_address', 'x_studio_address_2', 'x_studio_city', 'x_studio_zip_code', 'x_studio_field_O5d3J')
    def _compute_address_url(self):
        for task in self:
            url = "https://maps.google.com?q="
            if task.x_studio_address:
                url += task.x_studio_address
            if task.x_studio_address_2:
                url += task.x_studio_address_2
            if task.x_studio_city:
                url += '+' + task.x_studio_city
            if task.x_studio_zip_code:
                url += '+' + task.x_studio_zip_code
            if task.x_studio_field_O5d3J:
                url += '%2C' + task.x_studio_field_O5d3J
            task.x_studio_google_maps = url

    def action_view_bill(self):
        self.ensure_one()
        form = self.env.ref('account.view_move_form')
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "views": [[form.id, "form"]],
            "res_id": self.invoice_id.id,
            "context": {"create": False},
        }

    def _create_vendor_bill(self):
        """
        creating a vendor bill for a photographer.
        :return: bill
        """
        self = self.sudo()
        product = self.sale_line_id.product_id
        expense_lines = []
        account = product.product_tmpl_id._get_product_accounts()['expense']
        seller = product.seller_ids.filtered(lambda seller: seller.partner_id.id == self.photographer_id.partner_id.id and seller.product_id.id == product.id)

        if product.product_tmpl_id.billed_service_ok:
            expense_lines = self.sale_order_id.order_line.filtered(lambda line: not line.task_id and line.product_uom_qty > 0 and line.is_mto)
        
        bill = self.env['account.move'].create({
            'partner_id': self.photographer_id.partner_id.id,
            'move_type': 'in_invoice',
            'ref': self.name,
            'invoice_date': fields.Date.today(),
            'property_address': self.x_studio_property_address,
            'user_id': self.photographer_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'name': product.name,
                'quantity': 1,
                'account_id': account.id,
                'price_unit': seller and seller[-1].price or product.standard_price
            }), *[(0, 0, {
                'product_id': expense.product_id.id,
                'name': expense.product_id.name,
                'quantity': 1,
                'account_id': expense.product_id.product_tmpl_id._get_product_accounts()['expense'].id,
                'price_unit': expense.product_id.lst_price,
            }) for expense in expense_lines]]
        })

        bill._onchange_partner_id()
        # bill._onchange_payment_term_date_invoice()

        return bill

#Automated action : changing from rfq to po , create vendor bill for photo grapher.

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        if self.stage_id and self.stage_id.state == 'tour_completed':
            if self.sale_line_id and self.sale_line_id.order_id and self.sale_line_id.order_id.name:
                purchase_order = self.env['purchase.order'].search([('origin', '!=', False)])
                if purchase_order:
                    rec = purchase_order.search(
                        [('origin', '=', self.sale_line_id.order_id.name),
                         ('state', 'not in', ('cancel', 'purchase'))])
                    if rec:
                        rec.button_confirm()
                if self.sale_line_id.product_uom_qty > 0:
                    bill = self._origin._create_vendor_bill()
                    return {'value': {'invoice_id': bill.id}}
                return {}

    def write(self, values):
        for record in self:
            if record.sudo().invoice_id and record.sudo().invoice_id.state != 'cancel' and 'stage_id' in values:
                raise UserError(
                    _(" operation not permitted as task is already billed.\n"
                      " Please contact accounting department."))

            if values.get('stage_id') and not values.get('invoice_id'):
                stage = self.env['project.task.type'].browse(values.get('stage_id'))
                if stage.state == 'tour_completed' and record.sale_line_id and record.sale_line_id.product_uom_qty > 0:
                    bill = record._create_vendor_bill()
                    values['invoice_id'] = bill.id

        return super(ProjectTask, self).write(values)


