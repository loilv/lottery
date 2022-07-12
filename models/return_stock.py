from odoo import fields, api, models
from datetime import datetime
from odoo.exceptions import UserError, ValidationError


class ReturnStock(models.Model):
    _name = 'return.stock'

    name = fields.Char('Tên trả ế')
    date = fields.Date(string='Ngày', default=datetime.now())
    lines = fields.One2many('return.stock.line', 'return_stock_id')
    tele_ids = fields.One2many('return.stock.tele', 'return_stock_id')
    state = fields.Selection([('draft', 'Dự thảo'), ('done', 'Đã hoàn thành')], default='draft')

    @api.model
    def default_get(self, fields_list):
        res = super(ReturnStock, self).default_get(fields_list)
        stock_ids = self.env['data.tele'].search([])
        data = []
        for p in stock_ids:
            data.append((0, 0, {'data_tele_id': p.id}))
        res.update({'tele_ids': data})
        customer_ids = self.env['customer'].search([('status', '=', 'active')])
        val_lines = []
        for customer in customer_ids:
            vals = {
                'customer_id': customer.id,
            }
            val_lines.append((0, 0, vals))
        res.update({'lines': val_lines})
        return res

    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError('Không thể xóa phiếu trả ế đã hoàn thành')
        return super(ReturnStock, self).unlink()


class ReturnStockLine(models.Model):
    _name = "return.stock.line"

    return_stock_id = fields.Many2one('return.stock')
    customer_id = fields.Many2one('customer', string='Khách hàng', readonly=1)

    HCM = fields.Integer(string='TP HCM', default=0)
    HCM_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back")

    DT = fields.Integer(string='ĐT', sum="Tổng số")
    DT_PC = fields.Float(string='ĐT', readonly=1, compute="_compute_percent_back")

    CM = fields.Integer(string='CM')
    CM_PC = fields.Float(string='CM', readonly=1, compute="_compute_percent_back")

    BL = fields.Integer(string='BL')
    BL_PC = fields.Float(string='BL', readonly=1, compute="_compute_percent_back")

    BT = fields.Integer(string='BT')
    BT_PC = fields.Float(string='BT', readonly=1, compute="_compute_percent_back")

    VT = fields.Integer(string='VT')
    VT_PC = fields.Float(string='VT', readonly=1, compute="_compute_percent_back")

    ST = fields.Integer(string='ST')
    ST_PC = fields.Float(string='ST', readonly=1, compute="_compute_percent_back")

    CT = fields.Integer(string='ST')
    CT_PC = fields.Float(string='CT', readonly=1, compute="_compute_percent_back")

    DN = fields.Integer(string='ĐN')
    DN_PC = fields.Float(string='ĐN', readonly=1, compute="_compute_percent_back")

    TN = fields.Integer(string='TN')
    TN_PC = fields.Float(string='TN', readonly=1, compute="_compute_percent_back")

    AG = fields.Integer(string='AG')
    AG_PC = fields.Float(string='AG', readonly=1, compute="_compute_percent_back")

    BTH = fields.Integer(string='BTH')
    BTH_PC = fields.Float(string='BTH', readonly=1, compute="_compute_percent_back")

    BD = fields.Integer(string='BD')
    BD_PC = fields.Float(string='BD', readonly=1, compute="_compute_percent_back")

    TV = fields.Integer(string='TV')
    TV_PC = fields.Float(string='TV', readonly=1, compute="_compute_percent_back")

    VL = fields.Integer(string='VL')
    VL_PC = fields.Float(string='VL', readonly=1, compute="_compute_percent_back")

    HCM_2 = fields.Integer(string='TP HCM')
    HCM_2_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back")

    LA = fields.Integer(string='LA')
    LA_PC = fields.Float(string='LA', readonly=1, compute="_compute_percent_back")

    BP = fields.Integer(string='BP')
    BP_PC = fields.Float(string='BP', readonly=1, compute="_compute_percent_back")

    HG = fields.Integer(string='HG')
    HG_PC = fields.Float(string='HG', readonly=1, compute="_compute_percent_back")

    KG = fields.Integer(string='KG')
    KG_PC = fields.Float(string='KG', readonly=1, compute="_compute_percent_back")

    DL = fields.Integer(string='ĐL')
    DL_PC = fields.Float(string='ĐL', readonly=1, compute="_compute_percent_back")

    TG = fields.Integer(string='TG')
    TG_PC = fields.Float(string='TG', readonly=1, compute="_compute_percent_back")

    percent = fields.Float("%", compute="_compute_percent")
    sum_return = fields.Integer("Tổng trả", compute="_compute_sum_return")
    consume = fields.Integer("Tiêu thụ", compute="_compute_consume")
    ticket_receive = fields.Integer("Lượng vé lãnh", compute='_compute_ticket_receive')
    du_thieu = fields.Integer('Dư thiếu')
    revenues = fields.Integer('Tiền thu', compute="_compute_revenues")
    day_of_week = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ])

    date = fields.Date(string='Ngày', default=datetime.now())

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_sum_return(self):
        for r in self:
            if r.return_stock_id.day_of_week == '0':
                r.sum_return = (r.HCM + r.DT + r.CM)
            elif r.return_stock_id.day_of_week == '1':
                r.sum_return = (r.BL + r.BT + r.VT)
            elif r.return_stock_id.day_of_week == '2':
                r.sum_return = (r.ST + r.CT + r.DN)
            elif r.return_stock_id.day_of_week == '3':
                r.sum_return = (r.TN + r.AG + r.BTH)
            elif r.return_stock_id.day_of_week == '4':
                r.sum_return = (r.BD + r.TV + r.VL)
            elif r.return_stock_id.day_of_week == '5':
                r.sum_return = (r.HCM_2 + r.LA + r.BP + r.HG)
            else:
                r.sum_return = (r.KG + r.DL + r.TG)

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_consume(self):
        for r in self:
            plan = self.env['planed.line'].search(
                [('planed_id.date', '=', r.date), ('customer_id', '=', r.customer_id.id)])
            total = sum(plan.mapped('total'))
            r.consume = total - r.sum_return * 10000

    @api.depends('return_stock_id', 'return_stock_id.day_of_week')
    def _compute_ticket_receive(self):
        for r in self:
            day_week = 0
            if r.customer_id.planed.code == 'now':
                day_week = str(r.return_stock_id.day_of_week)
            elif r.customer_id.planed.code == 'now_1':
                day_week = str(int(r.return_stock_id.day_of_week) + 1)
            elif r.customer_id.planed.code == 'now_2':
                day_week = str(int(r.return_stock_id.day_of_week) + 2)
            elif r.customer_id.planed.code == 'now_3':
                day_week = str(int(r.return_stock_id.day_of_week) + 3)

            if day_week == '0':
                r.ticket_receive = (r.customer_id.HCM + r.customer_id.DT + r.customer_id.CM)
            elif day_week == '1':
                r.ticket_receive = (r.customer_id.BL + r.customer_id.BT + r.customer_id.VT)
            elif day_week == '2':
                r.ticket_receive = (r.customer_id.ST + r.customer_id.CT + r.customer_id.DN)
            elif day_week == '3':
                r.ticket_receive = (r.customer_id.TN + r.customer_id.AG + r.customer_id.BTH)
            elif day_week == '4':
                r.ticket_receive = (r.customer_id.BD + r.customer_id.TV + r.customer_id.VL)
            elif day_week == '5':
                r.ticket_receive = (r.customer_id.HCM_2 + r.customer_id.LA + r.customer_id.BP + r.customer_id.HG)
            else:
                r.ticket_receive = (r.customer_id.KG + r.customer_id.DL + r.customer_id.TG)

    @api.depends('ticket_receive', 'sum_return', 'du_thieu')
    def _compute_revenues(self):
        for r in self:
            province = self.env['province.lottery'].search([('group', '=', r.return_stock_id.day_of_week)])
            revenues = r.ticket_receive
            list_code = []
            if r.HCM > 0:
                price = province.filtered(lambda x: x.code == 'HCM').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.DT > 0:
                price = province.filtered(lambda x: x.code == 'DT').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.CM > 0:
                price = province.filtered(lambda x: x.code == 'CM').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.BL > 0:
                price = province.filtered(lambda x: x.code == 'BL').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.BT > 0:
                price = province.filtered(lambda x: x.code == 'BT').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.VT > 0:
                price = province.filtered(lambda x: x.code == 'VT').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu)  * price
            if r.ST > 0:
                price = province.filtered(lambda x: x.code == 'ST').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.CT > 0:
                price = province.filtered(lambda x: x.code == 'CT').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.DN > 0:
                price = province.filtered(lambda x: x.code == 'DN').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.TN > 0:
                price = province.filtered(lambda x: x.code == 'TN').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.AG > 0:
                price = province.filtered(lambda x: x.code == 'AG').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.BTH > 0:
                price = province.filtered(lambda x: x.code == 'BTH').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.BD > 0:
                price = province.filtered(lambda x: x.code == 'BD').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.TV > 0:
                price = province.filtered(lambda x: x.code == 'TV').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.VL > 0:
                price = province.filtered(lambda x: x.code == 'VL').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.HCM_2 > 0:
                price = province.filtered(lambda x: x.code == 'HCM_2').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.LA > 0:
                price = province.filtered(lambda x: x.code == 'LA').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.BP > 0:
                price = province.filtered(lambda x: x.code == 'BP').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.HG > 0:
                price = province.filtered(lambda x: x.code == 'HG').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.KG > 0:
                price = province.filtered(lambda x: x.code == 'KG').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.DL > 0:
                price = province.filtered(lambda x: x.code == 'DL').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            if r.TG > 0:
                price = province.filtered(lambda x: x.code == 'TG').price
                revenues -= ((r.sum_return * 10000) + r.du_thieu) * price
            r.revenues = revenues

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_percent_back(self):
        for r in self:
            r.HCM_PC = ((r.HCM * 10000) / r.customer_id.HCM) * 100 if r.customer_id.HCM > 0 else 0
            r.DT_PC = ((r.DT * 10000) / r.customer_id.DT) * 100 if r.customer_id.DT > 0 else 0
            r.CM_PC = ((r.CM * 10000) / r.customer_id.CM) * 100 if r.customer_id.CM > 0 else 0
            r.BL_PC = ((r.BL * 10000) / r.customer_id.BL) * 100 if r.customer_id.BL > 0 else 0
            r.BT_PC = ((r.BT * 10000) / r.customer_id.BT) * 100 if r.customer_id.BT > 0 else 0
            r.VT_PC = ((r.VT * 10000) / r.customer_id.VT) * 100 if r.customer_id.VT > 0 else 0
            r.ST_PC = ((r.ST * 10000) / r.customer_id.ST) * 100 if r.customer_id.ST > 0 else 0
            r.CT_PC = ((r.CT * 10000) / r.customer_id.CT) * 100 if r.customer_id.CT > 0 else 0
            r.DN_PC = ((r.DN * 10000) / r.customer_id.DN) * 100 if r.customer_id.DN > 0 else 0
            r.TN_PC = ((r.TN * 10000) / r.customer_id.TN) * 100 if r.customer_id.TN > 0 else 0
            r.AG_PC = ((r.AG * 10000) / r.customer_id.AG) * 100 if r.customer_id.AG > 0 else 0
            r.BTH_PC = ((r.BTH * 10000) / r.customer_id.BTH) * 100 if r.customer_id.BTH > 0 else 0
            r.BD_PC = ((r.BD * 10000) / r.customer_id.BD) * 100 if r.customer_id.BD > 0 else 0
            r.TV_PC = ((r.TV * 10000) / r.customer_id.TV) * 100 if r.customer_id.TV > 0 else 0
            r.VL_PC = ((r.VL * 10000) / r.customer_id.VL) * 100 if r.customer_id.VL > 0 else 0
            r.HCM_2_PC = ((r.HCM_2 * 10000) / r.customer_id.HCM_2) * 100 if r.customer_id.HCM_2 > 0 else 0
            r.LA_PC = ((r.LA * 10000) / r.customer_id.LA) * 100 if r.customer_id.LA > 0 else 0
            r.BP_PC = ((r.BP * 10000) / r.customer_id.BP) * 100 if r.customer_id.BP > 0 else 0
            r.HG_PC = ((r.HG * 10000) / r.customer_id.HG) * 100 if r.customer_id.HG > 0 else 0
            r.KG_PC = ((r.KG * 10000) / r.customer_id.KG) * 100 if r.customer_id.KG > 0 else 0
            r.DL_PC = ((r.DL * 10000) / r.customer_id.DL) * 100 if r.customer_id.DL > 0 else 0
            r.TG_PC = ((r.TG * 10000) / r.customer_id.TG) * 100 if r.customer_id.TG > 0 else 0

    @api.depends('HCM_PC', 'DT_PC', 'CM_PC', 'BL_PC', 'BT_PC', 'VT_PC', 'ST_PC', 'CT_PC', 'DN_PC', 'TN_PC', 'AG_PC',
                 'BTH_PC', 'BD_PC', 'TV_PC', 'VL_PC', 'HCM_2_PC', 'LA_PC', 'BP_PC', 'HG_PC', 'KG_PC', 'DL_PC', 'TG_PC')
    def _compute_percent(self):
        for r in self:
            if r.return_stock_id.day_of_week == '0':
                r.percent = (r.HCM_PC + r.DT_PC + r.CM_PC) / 3
            elif r.return_stock_id.day_of_week == '1':
                r.percent = (r.BL_PC + r.BT_PC + r.VT_PC) / 3
            elif r.return_stock_id.day_of_week == '2':
                r.percent = (r.ST_PC + r.CT_PC + r.DN_PC) / 3
            elif r.return_stock_id.day_of_week == '3':
                r.percent = (r.TN_PC + r.AG_PC + r.BTH_PC) / 3
            elif r.return_stock_id.day_of_week == '4':
                r.percent = (r.BD_PC + r.TV_PC + r.VL_PC) / 3
            elif r.return_stock_id.day_of_week == '5':
                r.percent = (r.HCM_2_PC + r.LA_PC + r.BP_PC + r.HG_PC) / 3
            else:
                r.percent = (r.KG_PC + r.DL_PC + r.TG_PC) / 3


class DataTele(models.Model):
    _name = "data.tele"

    name = fields.Char('Đài')
    code = fields.Char('Code')


class ReturnStockTele(models.Model):
    _name = "return.stock.tele"

    return_stock_id = fields.Many2one('return.stock')
    data_tele_id = fields.Many2one('data.tele', "Đài", readonly=1)

    HCM = fields.Char(string='TP HCM', compute="_compute_tele_value")
    DT = fields.Char(string='ĐT', compute="_compute_tele_value")
    CM = fields.Char(string='CM', compute="_compute_tele_value")
    BL = fields.Char(string='CM', compute="_compute_tele_value")
    BT = fields.Char(string='BT', compute="_compute_tele_value")
    VT = fields.Char(string='VT', compute="_compute_tele_value")
    ST = fields.Char(string='ST', compute="_compute_tele_value")
    CT = fields.Char(string='ST', compute="_compute_tele_value")
    DN = fields.Char(string='ĐN', compute="_compute_tele_value")
    TN = fields.Char(string='TN', compute="_compute_tele_value")
    AG = fields.Char(string='AG', compute="_compute_tele_value")
    BTH = fields.Char(string='BTH', compute="_compute_tele_value")
    BD = fields.Char(string='BD', compute="_compute_tele_value")
    TV = fields.Char(string='TV', compute="_compute_tele_value")
    VL = fields.Char(string='VL', compute="_compute_tele_value")
    HCM_2 = fields.Char(string='TP HCM', compute="_compute_tele_value")
    LA = fields.Char(string='LA', compute="_compute_tele_value")
    BP = fields.Char(string='BP', compute="_compute_tele_value")
    HG = fields.Char(string='HG', compute="_compute_tele_value")
    KG = fields.Char(string='KG', compute="_compute_tele_value")
    DL = fields.Char(string='ĐL', compute="_compute_tele_value")
    TG = fields.Char(string='TG', compute="_compute_tele_value")

    @api.depends('return_stock_id', 'return_stock_id.lines')
    def _compute_tele_value(self):
        for r in self:
            if r.data_tele_id.code == 'slte':
                r.HCM = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HCM')) * 10000)
                r.DT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DT')) * 10000)
                r.CM = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('CM')) * 10000)
                r.BL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BL')) * 10000)
                r.BT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BT')) * 10000)
                r.VT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('VT')) * 10000)
                r.ST = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('ST')) * 10000)
                r.CT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('CT')) * 10000)
                r.DN = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DN')) * 10000)
                r.TN = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TN')) * 10000)
                r.AG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('AG')) * 10000)
                r.BTH = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BTH')) * 10000)
                r.BD = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BD')) * 10000)
                r.TV = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TV')) * 10000)
                r.VL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('VL')) * 10000)
                r.HCM_2 = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HCM_2')) * 10000)
                r.LA = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('LA')) * 10000)
                r.BP = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BP')) * 10000)
                r.HG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HG')) * 10000)
                r.KG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('KG')) * 10000)
                r.DL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DL')) * 10000)
                r.TG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TG')) * 10000)
            elif r.data_tele_id.code == 'tl':
                r.HCM = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('HCM')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.DT = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('DT')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.CM = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('CM')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.BL = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('BL')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.BT = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('BT')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.VT = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('VT')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.ST = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('ST')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.CT = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('CT')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.DN = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('DN')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.TN = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('TN')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.AG = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('AG')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.BTH = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('BTH')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.BD = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('BD')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.TV = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('TV')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.VL = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('VL')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.HCM_2 = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('HCM_2')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.LA = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('LA')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.BP = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('BP')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.HG = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('HG')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.KG = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('KG')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.DL = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('DL')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
                r.TG = "{:,.0f}%".format((sum(r.return_stock_id.lines.mapped('TG')) / sum(
                    r.return_stock_id.lines.mapped('sum_return')) * 100)) if sum(
                    r.return_stock_id.lines.mapped('sum_return')) > 0 else 0
            else:
                r.HCM = ''
                r.DT = ''
                r.CM = ''
                r.BL = ''
                r.BT = ''
                r.VT = ''
                r.ST = ''
                r.CT = ''
                r.DN = ''
                r.TN = ''
                r.AG = ''
                r.BTH = ''
                r.BD = ''
                r.TV = ''
                r.VL = ''
                r.HCM_2 = ''
                r.LA = ''
                r.BP = ''
                r.HG = ''
                r.KG = ''
                r.DL = ''
                r.TG = ''
