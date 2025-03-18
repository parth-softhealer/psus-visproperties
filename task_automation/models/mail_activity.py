# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class MailActivity(models.Model):
  
    _inherit = 'mail.activity'

#Auto fill the location with the corresponding property address in the task

    def action_create_calendar_event(self):
        self.ensure_one()
        action = super(MailActivity, self).action_create_calendar_event()
        if self.env.context.get('default_res_model') == 'project.task':
            res_id = self.env.context.get('default_res_id')
            project_task_id = self.env['project.task'].browse(res_id)
            action['context'].update({'default_location':project_task_id.x_studio_property_address})
        return action

#Change the state from 'New Order' to 'Scheduled' once the scheduled activity option completed
 
    @api.model_create_multi
    def create(self, vals_list):
        activities = super(MailActivity, self).create(vals_list)
        project_tasks_ids = activities.filtered(lambda r: r.res_model_id.model == 'project.task').mapped('res_id')
        tasks = self.env['project.task'].browse(project_tasks_ids)
        if tasks:
            stages = self.env['project.task.type'].search([('state', '=', 'scheduled')])
            for task in tasks:
                if task.stage_id and task.stage_id.state and task.stage_id.state == 'new_order':
                    stage = stages.filtered(lambda rec: task.project_id in rec.project_ids)
                    if stage:
                        task.write({'stage_id': stage.ids[0]})
        return activities
