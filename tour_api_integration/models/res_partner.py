# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import logging
tour_api_url = 'https://api.tourwizard.net/'

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    tour_userid = fields.Char(string='Tour User Id')




class ChangePasswordUser(models.TransientModel):
    """ A model to configure users in the change password wizard. """
    _inherit = 'change.password.user'

    def change_password_button(self):
        for line in self:
            if not line.new_passwd:
                raise UserError(_("Before clicking on 'Change Password', you have to write a new password."))
            line.user_id.write({'password': line.new_passwd})
            if line.user_id.partner_id.tour_userid:
                payload = {'password': line.new_passwd}
                line.sudo().user_id.update_tour_user(payload)
            else:
                line.user_id.create_tour_user(line.user_id.login, line.new_passwd)
        self.write({'new_passwd': False})


class ResUsers(models.Model):
    _inherit = 'res.users'

    def update_tour_user(self, payload):
        self.ensure_one()
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        token = self.env.user.company_id.tour_api_key
        url = tour_api_url + 'v1/user/%s?access-token=%s' % (self.partner_id.tour_userid, token)
        _logger.info('Tour User Update...')
        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
            files=[]
        ).json()
        _logger.info(response)
        if not isinstance(response, dict):
            raise UserError('Invalid response')

    def create_tour_user(self, login, password):
        partner = self.partner_id
        name_list = partner.name.split(' ', 1)
        f_name = name_list[0] or False
        l_name = name_list[-1] or False
        token = self.env.user.company_id.tour_api_key
        url = tour_api_url + "v1/user?access-token=%s" % token
        payload = {
            'username': login,
            'role_id': '7' if self.share else '10',
            'first_name': f_name,
            'last_name': l_name,
            'email': login,
            'phone': partner.phone,
            'email_credentials': 1,
            'password': password
            }
        response = requests.request("POST", url, headers={}, data=payload).json()
        _logger.info('User creation from odoo')
        _logger.info(payload)
        _logger.info(response)
        if isinstance(response, dict):
            if response['data'].get('errors'):
                self.env.cr.rollback()
                if isinstance(response['data'].get('errors'), str):
                    raise UserError(response['data'].get('errors'))
                raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))
            partner.write({'tour_userid': response.get('data') and response['data']['id']})

    @api.model
    def signup(self, values, token=None):
        db, login, password = super(ResUsers, self).signup(values, token)
        user = self.search([('login', '=', login)], limit=1)
        if user.partner_id.tour_userid and password:
            payload = {'password': password}
            user.sudo().update_tour_user(payload)
        else:
            user.create_tour_user(login, password)
        return db, login, password
