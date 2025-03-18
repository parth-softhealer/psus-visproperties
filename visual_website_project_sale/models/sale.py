from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    photographer_id = fields.Many2one('res.users', 'Photographer',domain="[('share','=',False)]")
  
    def write(self,vals):
        res = super(SaleOrder,self).write(vals)
        if 'photographer_id' in vals and vals.get('photographer_id'):
            for sale in self: 
                if not self.env.context.get('no_sale_update'):
                    sale.tasks_ids.with_context(no_sale_update= True).write({'photographer_id': sale.photographer_id.id})
                purchase_order_ids = self.env['purchase.order'].search([('group_id', '=', sale.procurement_group_id.id), ('state','in', ('draft', 'sent') )])
                if purchase_order_ids:
                    purchase_order_ids.write({'partner_id': sale.photographer_id.partner_id.id})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_task_prepare_values(self, project):
        self.ensure_one()
        res = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(project)
        order = project.sale_line_id and project.sale_line_id.order_id or self.order_id
        res.update({'photographer_id': order.photographer_id.id if order.photographer_id else False,
                    'user_ids':[order.photographer_id.id] if order.photographer_id else False})
        return res

    @api.depends('product_id')
    def _compute_is_service(self):
        for so_line in self:
            is_service = False
            if so_line.product_id.type in ['service', 'consu']:
                is_service = True
            so_line.is_service = is_service
