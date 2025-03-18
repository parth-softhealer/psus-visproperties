# -*- encoding: utf-8 -*-

import requests
from odoo.exceptions import UserError

from odoo import fields, models


class ResCompany(models.Model):
    
    _inherit = "res.company"

    tour_api_key = fields.Char(string='Tour Api Key')
    tour_backend_url = fields.Char(string='Edit Url', default='http://team.visualproperties.net/tour/dashboard/$TOURID')


    def sync_users(self):

        partner_data = []

        if not self.tour_api_key:
            raise UserError("Choose a key inside the company")

        url = 'https://api.tourwizard.net/v1/user?access-token=%s' % (self.tour_api_key)

        while True:
            response = requests.request("GET", url).json()
            if response['data']['items']:
                partner_data.extend(response['data']['items'])
                if response['data']['links'].get('next'):
                    next_data = response['data']['links'].get('next')
                    url = next_data.get('href')
                else:
                    break

        partners = self.env['res.partner'].search([])
        for partner in partners:
            partner_info = list(
                filter(lambda rec: rec['username'] == partner.email or rec['profile']['email'] == partner.email,
                       partner_data))
            if partner_info:
                partner.write({'tour_userid': partner_info[-1].get('id')})


