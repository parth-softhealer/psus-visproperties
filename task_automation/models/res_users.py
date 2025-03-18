from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.constrains('login')
    def _check_duplicate_login(self):
        for rec in self:
            emails = self.env['res.users'].search_count(
                [('login', '=', rec.login), ('active', '=', True)]
                )
            if emails > 1:
                raise ValidationError(
                    "You can not have two users with the same login!"
                    )


class ResCompany(models.Model):
    _inherit = "res.company"

    iguide_hook_url = fields.Char(
        string='iGuide Hook Url', compute='_compute_iguide_hook_url'
        )

    def _compute_iguide_hook_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url'
            )
        url = base_url + '/webhook'
        for rec in self:
            rec.iguide_hook_url = url
