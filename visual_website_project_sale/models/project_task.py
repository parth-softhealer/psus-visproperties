from odoo import fields, models, _

class ProjectTask(models.Model):
    _inherit = 'project.task'
    photographer_id = fields.Many2one(comodel_name='res.users', string='Photographer', domain="[('share','=',False)]") 

    def write(self,vals):
        if 'photographer_id' in vals and vals.get('photographer_id'):
            vals['user_ids'] = [vals['photographer_id']]
        res = super(ProjectTask,self).write(vals)
        if 'photographer_id' in vals and vals.get('photographer_id') and not self.env.context.get('no_sale_update'):
            for task in self:
                task.sale_order_id.with_context(no_sale_update = True).write({'photographer_id': task.photographer_id.id}) 
        return res
