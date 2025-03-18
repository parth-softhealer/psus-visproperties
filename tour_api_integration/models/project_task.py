# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import  UserError
import requests

tour_api_url = 'https://api.tourwizard.net/'


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_media_uploaded = fields.Boolean(string="Is media uploaded")
    is_cancel = fields.Boolean(string="Is Cancel")





class ProjectTask(models.Model):
    _inherit = 'project.task'

    tour_id = fields.Char(string='Tour Id')
    tour_link = fields.Char(string='Tour Link')
    client_tour_id = fields.Char(string='Client Tour Id')
    is_reshoot = fields.Boolean(string="Is Reshoot")
    backend_url = fields.Char(string="Edit Url", compute='_compute_backend_url')

    def write(self, vals):

        res = super(ProjectTask, self).write(vals)
        if 'stage_id' in vals:
            stage = self.env['project.task.type'].browse(vals.get('stage_id'))
            for task in self:
                if stage.is_media_uploaded and not task.tour_id and not task.is_reshoot and task.sale_line_id and not task.sale_line_id.product_id.exclude_tour_creation:
                    task.company_id and task.company_id.sudo().sync_users()
                    client_tour_id, auto_login, brand_url, unbrand_url = task._tour_api()
                    task.tour_id = client_tour_id
                    task.x_studio_client_tours = auto_login
                    task.x_studio_branded_tour = brand_url
                    task.x_studio_un_branded_tour = unbrand_url
                elif stage.is_cancel and task.tour_id:

                    if not task.company_id.tour_api_key:
                        raise UserError("Choose a key inside the company")
                    token = task.company_id and task.company_id.tour_api_key
                    url = tour_api_url + "v1/tour/%s?access-token=%s" % (str(task.tour_id), token)

                    payload = 'status_id=4'
                    headers = {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    }
                    response = requests.request("PUT", url, headers=headers, data=payload).json()
                    if not isinstance(response, dict):
                        raise UserError('Invalid response')
                    if response.get('success'):
                        template = self.env.ref('tour_api_integration.mail_template_project_task_cancel')
                        task.message_post_with_template(template.id, notif_layout="mail.mail_notification_light")
        return res

    def _compute_backend_url(self):
        for task in self:
            if task.tour_id:
                task.backend_url = task.company_id.tour_backend_url.replace('$TOURID', task.tour_id)
            else:
                task.backend_url = False

    def _tour_api(self):

        self.ensure_one()

        name_list = self.partner_id and self.partner_id.name.split(' ', 1)
        f_name = name_list[0] or False
        l_name = name_list[-1] or False

        photographer_name_list = self.photographer_id.partner_id and self.photographer_id.partner_id.name.split(' ', 1)
        fp_name = photographer_name_list[0] or False
        lp_name = photographer_name_list[-1] or False

        if not self.company_id.tour_api_key:
            raise UserError("Choose a key inside the company")
        token = self.company_id and self.company_id.tour_api_key
        client_tour_id = auto_login = brand_url = unbrand_url = ''

        if not self.partner_id.email:
            raise UserError("Partner Email doesnot Found")

        # Create a user if doesnot exists
        if self.partner_id and not self.partner_id.tour_userid:
            url = tour_api_url + "v1/user?access-token=%s" % (token)
            payload = {
                'username': self.partner_id.email,
                'role_id': '7',
                'first_name': f_name,
                'last_name': l_name,
                'email': self.partner_id.email,
                'phone': self.partner_id.phone,
                'email_credentials': 1
            }
            response = requests.request("POST", url, headers={}, data=payload).json()

            if isinstance(response, dict):
                if response['data'].get('errors'):
                    if isinstance(response['data'].get('errors'), str):
                        raise UserError(response['data'].get('errors'))
                    raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))
                self.partner_id.write({'tour_userid': response.get('data') and response['data']['id']})
        url = tour_api_url + "v1/user/%s?access-token=%s" % (str(self.partner_id.tour_userid), token)
        response = requests.request("GET", url, headers={}, data={}).json()

        if isinstance(response, dict) and response['data'].get('errors'):
            if isinstance(response['data'].get('errors'), str):
                raise UserError(response['data'].get('errors'))
            raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))

        if isinstance(response, dict) and response.get('success'):
            auto_login = response['data']['auto_login']

        # Create a photographer if doesnot exists

        if self.photographer_id.partner_id and not self.photographer_id.partner_id.tour_userid:
            url = tour_api_url + "v1/user?access-token=%s" % (token)
            payload = {
                'username': self.photographer_id.partner_id.email,
                'role_id': '10',
                'first_name': fp_name,
                'last_name': lp_name,
                'email': self.photographer_id.partner_id.email,
                'phone': self.photographer_id.partner_id.phone,
                'email_credentials': 1
            }

            response = requests.request("POST", url, headers={}, data=payload).json()

            if isinstance(response, dict):
                if response['data'].get('errors'):
                    if isinstance(response['data'].get('errors'), str):
                        raise UserError(response['data'].get('errors'))
                    raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))
                self.photographer_id.partner_id.write({'tour_userid': response.get('data') and response['data']['id']})

        url = tour_api_url + "v1/tour?access-token=%s" % (token)
        from pprint import pprint

        payload = {
            'user_id': int(self.partner_id.tour_userid),
            'address': "%s %s" % (self.x_studio_address or "", self.x_studio_address_2 or ""),
            'postal_code': self.x_studio_field_O5d3J or '',
            'city': self.x_studio_city,
            'state': self.x_studio_zip_code,
            'design_id': '2',
            'photographer_id': int(self.photographer_id.partner_id.tour_userid),
            'on_ready_status': 20,
            'status_id': 20
        }

        response = requests.request("POST", url, headers={}, data=payload).json()

        if isinstance(response, dict) and response['data'].get('errors'):
            if isinstance(response['data'].get('errors'), str):
                raise UserError(response['data'].get('errors'))
            raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))
        if not isinstance(response, dict):
            raise UserError('Invalid response')

        client_tour_id = response.get('success') and response['data']['id']
        url = tour_api_url + "v1/tour/%s?access-token=%s" % (client_tour_id, token)
        response = requests.request("GET", url, headers={}, data={}).json()

        if not isinstance(response, dict):
            raise UserError('Invalid response')
        if response['data'].get('errors'):
            if isinstance(response['data'].get('errors'), str):
                raise UserError(response['data'].get('errors'))
            raise UserError('\n'.join(sum(list(response['data']['errors'].values()), [])))

        if response.get('success'):
            brand_url, unbrand_url = response['data']['branded_url'], response['data']['unbranded_url']

        return client_tour_id, auto_login, brand_url, unbrand_url
