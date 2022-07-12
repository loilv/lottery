import json

from lxml import etree
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from odoo import fields, api, models, _


class Planed(models.Model):
    _name = 'planed'
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
                'AG': customer.AG,
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
        res.update({'lines': val_lines})
        return res

    name = fields.Char(string='Tên kế hoạch', default='')
    date = fields.Date(string='Ngày', default=datetime.now())
    lines = fields.One2many('planed.line', 'planed_id', string='Chi tiết')
    state = fields.Selection([('draft', 'Dự thảo'), ('done', 'Đã hoàn thành')], default='draft')

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
        plan = self.search([('state', '!=', 'done')])
        for item in plan:
            item.state = 'done'
        purchase = self.env['purchase.inventory'].search([('state', '!=', 'done')])
        for item in purchase:
            item.state = 'done'
        re_stock = self.env['return.stock'].search([('state', '!=', 'done')])
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

    total = fields.Integer(string='Tổng số vé', compute='_compute_total')
    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])

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
                item.total = (item.HCM_2 + item.LA + item.BP + item.HG) + (item.HCM_2_PS + item.LA_PS + item.BP_PS + item.HG_PS)
            elif item.planed_id.day_of_week == '6':
                item.total = (item.KG + item.DL + item.TG) + (item.KG_PS + item.DL_PS + item.TG_PS)
            else:
                item.total = 0
            item.total = item.total