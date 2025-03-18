# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class Meeting(models.Model):
   
    _inherit = 'calendar.event'

    location = fields.Text(string='Location')

    @api.model_create_multi
    def create(self, list_vals):
        meetings = super(Meeting, self).create(list_vals)
        meeting_ids = meetings.filtered(lambda r: r.res_model == 'project.task').mapped('res_id')
        if meeting_ids:
            tasks = self.env['project.task'].browse(meeting_ids)
            for task in tasks:
                for meeting in meetings:
                    if meeting.res_id == task.id:
                        task.x_studio_field_KRr2Q = meeting
        return meetings


