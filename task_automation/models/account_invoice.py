# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_address = fields.Char(string='Property address')
