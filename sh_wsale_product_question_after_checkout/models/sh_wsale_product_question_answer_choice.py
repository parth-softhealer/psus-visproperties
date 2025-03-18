# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, models, fields, _
from odoo.exceptions import UserError

class QuestionAnswerChoice(models.Model):

    _name = 'sh.wsale.product.question.answer.choice'
    _order = 'sequence,id'
    _description = 'Question Answer Choice'

    name = fields.Char('Answer',  translate=True)
    question_id = fields.Many2one('sh.wsale.product.question', ondelete='cascade')
    sequence = fields.Integer(default=10)
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_selected_answer(self):
        if self.env['sh.wsale.product.question.answer'].search_count([('value_answer_id', 'in', self.ids)]):
            raise UserError(_('You cannot delete an answer that has already been selected by attendees.'))
