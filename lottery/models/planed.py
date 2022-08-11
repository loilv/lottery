import json

from lxml import etree
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
from odoo import fields, api, models, _


class Planed(models.Model):
    _name = 'planed'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    @api.model
    def default_get(self, fields_list):
        res = super(Planed, self).default_get(fields_list)
        customer_ids = self.env['customer'].search([('status', '=', 'active')])
        val_lines = []
        for customer in customer_ids:
            vals = {
                'customer_id': customer.id,
                'HCM': customer.HCM,
                'DT': customer.DT,
                'CM': customer.CM,
                'BL': customer.BL,
                'BT': customer.BT,
                'VT': customer.VT,
                'ST': customer.ST,
                'CT': customer.CT,
                'DN': customer.DN,
                'TN': customer.TN,
                'AG': customer.AG,
                'BTH': customer.BTH,
                'BD': customer.BD,
                'TV': customer.TV,
                'VL': customer.VL,
                'HCM_2': customer.HCM_2,
                'LA': customer.LA,
                'BP': customer.BP,
                'HG': customer.HG,
                'KG': customer.KG,
                'DL': customer.DL,
                'TG': customer.TG,
            }
            val_lines.append((0, 0, vals))
        inventory = self.env['purchase.inventory'].search([('date', '=', self._context.get('default_date'))], limit=1)
        stock_vals = []
        quantities = self.env['purchase.inventory'].get_total(date=self._context.get('default_date'))
        for item in inventory.lines:
            code = item.province_id.code
            vals = {
                'province_id': item.province_id.id,
                'quantity_in': quantities[code],
                'quantity_out': quantities[code] - sum(customer_ids.mapped(code)),
            }
            stock_vals.append((0, 0, vals))
        res.update({'stock_info': stock_vals, 'lines': val_lines})
        return res

    name = fields.Char(string='Tên kế hoạch', default='')
    date = fields.Date(string='Ngày', default=lambda self: fields.Datetime.now())
    lines = fields.One2many('planed.line', 'planed_id', string='Chi tiết')
    state = fields.Selection([('draft', 'Dự thảo'), ('done', 'Đã hoàn thành')], default='draft')
    stock_info = fields.One2many('stock.information', 'planed_id', string='Tồn kho')

    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])

    def update_state_lottery(self):
        plan = self.search([('state', '!=', 'done'), ('date', '<', date.today())])
        for item in plan:
            item.state = 'done'
        purchase = self.env['purchase.inventory'].search([('state', '!=', 'done'), ('date', '<', date.today())])
        for item in purchase:
            item.state = 'done'
        re_stock = self.env['return.stock'].search([('state', '!=', 'done'), ('date', '<', date.today())])
        for item in re_stock:
            item.state = 'done'

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError('Không thể xóa kế hoạch đã hoàn thành')
        return super(Planed, self).unlink()


class PlanedLine(models.Model):
    _name = 'planed.line'
    _description = 'Kế hoạch lãnh vé'

    planed_id = fields.Many2one('planed')

    customer_id = fields.Many2one('customer', string='Khách hàng', readonly=1)
    HCM = fields.Integer(string='TP HCM', readonly=1)
    HCM_PS = fields.Integer(string='TP HCM(PS)')

    DT = fields.Integer(string='ĐT', readonly=1, sum="Tổng số")
    DT_PS = fields.Integer(string='ĐT(PS)')

    CM = fields.Integer(string='CM', readonly=1)
    CM_PS = fields.Integer(string='CM(PS)')

    BL = fields.Integer(string='CM', readonly=1)
    BL_PS = fields.Integer(string='BL(PS)')

    BT = fields.Integer(string='BT', readonly=1)
    BT_PS = fields.Integer(string='BT(PS)')

    VT = fields.Integer(string='VT', readonly=1)
    VT_PS = fields.Integer(string='VT(PS)')

    ST = fields.Integer(string='ST', readonly=1)
    ST_PS = fields.Integer(string='ST(PS)')

    CT = fields.Integer(string='ST', readonly=1)
    CT_PS = fields.Integer(string='CT(PS)')

    DN = fields.Integer(string='ĐN', readonly=1)
    DN_PS = fields.Integer(string='ĐN(PS)')

    TN = fields.Integer(string='TN', readonly=1)
    TN_PS = fields.Integer(string='TN(PS)')

    AG = fields.Integer(string='AG', readonly=1)
    AG_PS = fields.Integer(string='AG(PS)')

    BTH = fields.Integer(string='BTH', readonly=1)
    BTH_PS = fields.Integer(string='BTH(PS)')

    BD = fields.Integer(string='BD', readonly=1)
    BD_PS = fields.Integer(string='BD(PS)')

    TV = fields.Integer(string='TV', readonly=1)
    TV_PS = fields.Integer(string='TV(PS)')

    VL = fields.Integer(string='VL', readonly=1)
    VL_PS = fields.Integer(string='VL(PS)')

    HCM_2 = fields.Integer(string='TP HCM', readonly=1)
    HCM_2_PS = fields.Integer(string='TP HCM(PS)')

    LA = fields.Integer(string='LA', readonly=1)
    LA_PS = fields.Integer(string='LA(PS)')

    BP = fields.Integer(string='BP', readonly=1)
    BP_PS = fields.Integer(string='BP(PS)')

    HG = fields.Integer(string='HG', readonly=1)
    HG_PS = fields.Integer(string='HG(PS)')

    KG = fields.Integer(string='KG', readonly=1)
    KG_PS = fields.Integer(string='KG(PS)')

    DL = fields.Integer(string='ĐL', readonly=1)
    DL_PS = fields.Integer(string='ĐL(PS)')

    TG = fields.Integer(string='TG', readonly=1)
    TG_PS = fields.Integer(string='TG(PS)')

    total = fields.Integer(string='Tổng số vé', compute='_compute_total', store=True)
    date = fields.Date(string='Ngày', related='planed_id.date')
    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ], compute="_compute_day_of_week", store=True)

    @api.depends('date')
    def _compute_day_of_week(self):
        for r in self:
            if r.date:
                r.day_of_week = str(r.date.weekday())

    @api.depends(
        'HCM_PS', 'DT_PS', 'CM_PS', 'BL_PS', 'BT_PS',
        'VT_PS', 'ST_PS', 'CT_PS', 'DN_PS', 'TN_PS',
        'AG_PS', 'BTH_PS', 'BD_PS', 'TV_PS', 'VL_PS',
        'HCM_2_PS', 'LA_PS', 'BP_PS', 'HG_PS', 'KG_PS',
        'DL_PS', 'TG_PS'
    )
    def _compute_total(self):
        for item in self:
            if item.planed_id.day_of_week == '0':
                item.total = (item.HCM + item.DT + item.CM) + (item.HCM_PS + item.DT_PS + item.CM_PS)
            elif item.planed_id.day_of_week == '1':
                item.total = (item.BL + item.BT + item.VT) + (item.BL_PS + item.BT_PS + item.VT_PS)
            elif item.planed_id.day_of_week == '2':
                item.total = (item.ST + item.CT + item.DN) + (item.ST_PS + item.CT_PS + item.DN_PS)
            elif item.planed_id.day_of_week == '3':
                item.total = (item.TN + item.AG + item.BTH) + (item.TN_PS + item.AG_PS + item.BTH_PS)
            elif item.planed_id.day_of_week == '4':
                item.total = (item.BD + item.TV + item.VL) + (item.BD_PS + item.TV_PS + item.VL_PS)
            elif item.planed_id.day_of_week == '5':
                item.total = (item.HCM_2 + item.LA + item.BP + item.HG) + (
                        item.HCM_2_PS + item.LA_PS + item.BP_PS + item.HG_PS)
            elif item.planed_id.day_of_week == '6':
                item.total = (item.KG + item.DL + item.TG) + (item.KG_PS + item.DL_PS + item.TG_PS)
            else:
                item.total = 0
            item.total = item.total


    def write(self, vals):
        d = self.total
        if self.day_of_week == '0':
            a = self.HCM_PS
            b = self.DT_PS
            c = self.CM_PS
            if vals.get('HCM_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'TP HCM(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('HCM_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('DT_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'DT(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('DT_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('CM_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'CM(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('CM_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '1':
            a = self.BL_PS
            b = self.BT_PS
            c = self.VT_PS
            if vals.get('BL_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'BL(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('BL_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('BT_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'BT(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('BT_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('VT_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'VT(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('VT_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '2':
            a = self.ST_PS
            b = self.CT_PS
            c = self.DN_PS
            if vals.get('ST_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'ST(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('ST_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('CT_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'CT(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('CT_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('DN_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'DN(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('DN_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '3':
            a = self.TN_PS
            b = self.AG_PS
            c = self.BTH_PS
            if vals.get('TN_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'TN(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('TN_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('AG_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'AG(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('AG_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('BTH_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'BTH(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('BTH_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '4':
            a = self.BD_PS
            b = self.TV_PS
            c = self.VL_PS
            if vals.get('BD_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'BD(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('BD_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('TV_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'TV(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('TV_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('VL_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'VL(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('VL_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '5':
            a = self.HCM_2_PS
            b = self.LA_PS
            c = self.BP_PS
            e = self.HG_PS
            if vals.get('HCM_2_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'TP HCM(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('HCM_2_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('LA_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'LA(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('LA_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('BP_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'BP(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('BP_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('HG_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'HG(PS)',
                                                              'ps_old': e,
                                                              'ps_new': vals.get('HG_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        if self.day_of_week == '6':
            a = self.KG_PS
            b = self.DL_PS
            c = self.TG_PS
            if vals.get('KG_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'KG(PS)',
                                                              'ps_old': a,
                                                              'ps_new': vals.get('KG_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('DL_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'DL(PS)',
                                                              'ps_old': b,
                                                              'ps_new': vals.get('DL_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
            if vals.get('TG_PS'):
                self.planed_id.message_post_with_view('lottery.message_change_ps',
                                                      values={'cus': self.customer_id.name,
                                                              'name': 'TG(PS)',
                                                              'ps_old': c,
                                                              'ps_new': vals.get('TG_PS')},
                                                      subtype_id=self.env.ref('mail.mt_note').id)
        self.planed_id.message_post_with_view('lottery.message_change_ps',
                                              values={'cus': self.customer_id.name,
                                                      'name': 'Tổng số vé',
                                                      'ps_old': d,
                                                      'ps_new': vals.get('total')},
                                              subtype_id=self.env.ref('mail.mt_note').id)
        res = super(PlanedLine, self).write(vals)
        return res


class StockInformation(models.Model):
    _name = 'stock.information'

    planed_id = fields.Many2one('planed', string='Kế hoạch')
    province_id = fields.Many2one('province.lottery', string='Tên đài', readonly=1)
    quantity_in = fields.Integer(string='Tổng nhập', readonly=1)
    quantity_out = fields.Integer(string='Tồn cuối', readonly=1)

    # @api.depends('quantity_in')
    # def handle_quantity(self):
    #     for item in self:
    #         if item.planed_id:
    #             try:
    #                 sum_amount = sum(item.planed_id.lines.mapped(item.province_id.code))
    #                 item.quantity_out = item.quantity_in - sum_amount
    #             except Exception as e:
    #                 item.quantity_out = 0
    #         else:
    #             item.quantity_out = 0