from odoo import fields, models, api


class ResCountry(models.Model):
    _inherit = 'res.country'

    def get_website_sale_countries(self, mode='billing'):
        res = super(ResCountry, self).get_website_sale_countries(mode)
        if not res:
            return self.sudo().search([])

        return res
