from odoo import fields, api, models, _
from datetime import datetime
from odoo.exceptions import RedirectWarning

class PurchaseInventoryWZ(models.TransientModel):
    _name = 'purchase.inventory.wz'

    date = fields.Date('Ngày nhập', default=datetime.now())

    def create_purchase(self):
        purchase = self.env['purchase.inventory'].search([('date', '=', self.date)], limit=1)
        if purchase:
            action = {
                'name': _('Phiếu nhập kho'),
                'view_mode': 'form',
                'res_model': 'planed',
                'type': 'ir.actions.act_window',
                'res_id': purchase.id,
                'views': [[self.env.ref('lottery.purchase_inventory_form_view').id, 'form'],
                          [self.env.ref('lottery.purchase_inventory_tree_view').id, 'list']],
                'target': 'current',
            }
            msg = _('Đã tồn phiếu nhập kho: %s.' % self.date.strftime("%d-%m-%Y"))
            raise RedirectWarning(msg, action, _('Đi tới phiếu nhập'))
        return {
            'name': _('Nhập kho'),
            'view_mode': 'form',
            'res_model': 'purchase.inventory',
            'type': 'ir.actions.act_window',
            'context': {
                'default_name': f'Nhập kho ngày: {self.date.strftime("%d-%m-%Y")}',
                'default_date': self.date,
                'default_day_of_week': str(self.date.weekday()),
            },
            'view_id': self.env.ref('lottery.purchase_inventory_form_view').id,
            'target': 'current',
        }