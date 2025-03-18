from odoo.addons.website_sale.controllers.main import WebsiteSale
# from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.http import request


# comment by softhealer

# class WebsiteSaleVisDelivery(WebsiteSaleDelivery):

#     def _get_shop_payment_values(self, order, **kwargs):
#         values = super(WebsiteSaleDelivery, self)._get_shop_payment_values(order, **kwargs)
#         has_storable_products = any(line.product_id.type == 'product' for line in order.order_line)
#         if not order._get_delivery_methods() and has_storable_products:
#             values['errors'].append(
#                 ('Sorry, we are unable to ship your order',
#                  'No shipping method is available for your current order and shipping address. '
#                    'Please contact us for more information.'))

#         if has_storable_products:
#             if order.carrier_id and not order.delivery_rating_success:
#                 order._remove_delivery_line()

#             delivery_carriers = order._get_delivery_methods()
#             values['deliveries'] = delivery_carriers.sudo()

#         values['delivery_has_storable'] = has_storable_products
#         values['delivery_action_id'] = request.env.ref('delivery.action_delivery_carrier_form').id
#         return values

class WebsiteSale(WebsiteSale):

    def values_postprocess(self, order, mode, values, errors, error_msg):

        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(order, mode, values, errors, error_msg)
        if 'type' in new_values and new_values.get('type') == 'delivery':
            new_values['type'] = 'other'
        return new_values, errors, error_msg

    def checkout_values(self, **kw):
        values = super(WebsiteSale, self).checkout_values(**kw)
        shippings = [ship for ship in values.get('shippings') if ship.type == 'delivery']
        values.update({
            'shippings': shippings
            })
        return values

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(WebsiteSale, self).checkout_form_validate( mode, all_form_values, data)
        Partner = request.env['res.partner']
        # Softhealer commented below code as per client task:
        
        #         Fix the email field so that if the same email address is used as the login
        # it doesn’t give the error “email already in use” message.
        # Not sure what it going on with this. 

        # Also do not need it to be a required field.
        # answer; it's a standard odoo flow you can't signup again with same email address.        
   


        # email validation
        # if request.env.user.partner_id.email != data.get('email'):
        #     if data.get('email') and Partner.sudo().search_count([('email', '=', data.get('email')), ('active', '=', True)]):
        #         error["email"] = 'duplicate'
        #         error_message.append('Email address already in use!  Please sign in or try another email address')

        return error, error_message
