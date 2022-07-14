from odoo import fields, api, models, _
from datetime import datetime
from odoo.exceptions import RedirectWarning


class CreateReturnStock(models.TransientModel):
    _name = 'create.return.stock'

    date = fields.Date('Trả ế ngày', default=datetime.now())

    def create_return_stock(self):
        return_stock = self.env['return.stock'].search([('date', '=', self.date)], limit=1)
        if return_stock:
            action = {
                'name': _('Kế hoạch lãnh vé'),
                'view_mode': 'form',
                'res_model': 'return.stock',
                'type': 'ir.actions.act_window',
                'res_id': return_stock.id,
                'views': [[self.env.ref('lottery.form_return_stock').id, 'form'],
                          [self.env.ref('lottery.tree_return_stock').id, 'list']],
                'target': 'current',
            }
            msg = _('Đã tồn tại chứng từ trả ế: %s.' % self.date.strftime("%d-%m-%Y"))
            raise RedirectWarning(msg, action, _('Đi tới chừng từ'))
        return {
            'name': _('Trả ế'),
            'view_mode': 'form',
            'res_model': 'return.stock',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': f'Trả ế ngày {self.date.strftime("%d-%m-%Y")}',
                'default_date': self.date,
                'default_day_of_week': str(self.date.weekday()),
            },
            'view_id': self.env.ref('lottery.form_return_stock').id,
            'target': 'current',
        }