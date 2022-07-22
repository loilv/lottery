from odoo import fields, api, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class ReturnStock(models.Model):
    _name = 'return.stock'

    name = fields.Char('Tên chứng từ trả ế')
    date = fields.Date(string='Ngày', default=datetime.now())
    lines = fields.One2many('return.stock.line', 'return_stock_id')
    tele_ids = fields.One2many('return.stock.tele', 'return_stock_id')
    state = fields.Selection([('draft', 'Dự thảo'), ('done', 'Đã hoàn thành')], default='draft')
    is_show = fields.Boolean(default=False)

    def action_show(self):
        if not self.is_show:
            self.is_show = True
        else:
            self.is_show = False

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

    HCM = fields.Integer(string='TP HCM (Tờ)', default=0)
    HCM_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back", store=True)

    DT = fields.Integer(string='ĐT (Tờ)', sum="Tổng số")
    DT_PC = fields.Float(string='ĐT', readonly=1, compute="_compute_percent_back", store=True)

    CM = fields.Integer(string='CM (Tờ)')
    CM_PC = fields.Float(string='CM', readonly=1, compute="_compute_percent_back", store=True)

    BL = fields.Integer(string='BL (Tờ)')
    BL_PC = fields.Float(string='BL', readonly=1, compute="_compute_percent_back", store=True)

    BT = fields.Integer(string='BT (Tờ)')
    BT_PC = fields.Float(string='BT', readonly=1, compute="_compute_percent_back", store=True)

    VT = fields.Integer(string='VT (Tờ)')
    VT_PC = fields.Float(string='VT', readonly=1, compute="_compute_percent_back", store=True)

    ST = fields.Integer(string='ST (Tờ)')
    ST_PC = fields.Float(string='ST', readonly=1, compute="_compute_percent_back", store=True)

    CT = fields.Integer(string='ST (Tờ)')
    CT_PC = fields.Float(string='CT', readonly=1, compute="_compute_percent_back", store=True)

    DN = fields.Integer(string='ĐN (Tờ)')
    DN_PC = fields.Float(string='ĐN', readonly=1, compute="_compute_percent_back", store=True)

    TN = fields.Integer(string='TN (Tờ)')
    TN_PC = fields.Float(string='TN', readonly=1, compute="_compute_percent_back", store=True)

    AG = fields.Integer(string='AG (Tờ)')
    AG_PC = fields.Float(string='AG', readonly=1, compute="_compute_percent_back", store=True)

    BTH = fields.Integer(string='BTH (Tờ)')
    BTH_PC = fields.Float(string='BTH', readonly=1, compute="_compute_percent_back", store=True)

    BD = fields.Integer(string='BD (Tờ)')
    BD_PC = fields.Float(string='BD', readonly=1, compute="_compute_percent_back", store=True)

    TV = fields.Integer(string='TV (Tờ)')
    TV_PC = fields.Float(string='TV', readonly=1, compute="_compute_percent_back", store=True)

    VL = fields.Integer(string='VL (Tờ)')
    VL_PC = fields.Float(string='VL', readonly=1, compute="_compute_percent_back", store=True)

    HCM_2 = fields.Integer(string='TP HCM (Tờ)')
    HCM_2_PC = fields.Float(string='TP HCM', readonly=1, compute="_compute_percent_back", store=True)

    LA = fields.Integer(string='LA (Tờ)')
    LA_PC = fields.Float(string='LA', readonly=1, compute="_compute_percent_back", store=True)

    BP = fields.Integer(string='BP (Tờ)')
    BP_PC = fields.Float(string='BP', readonly=1, compute="_compute_percent_back", store=True)

    HG = fields.Integer(string='HG (Tờ)')
    HG_PC = fields.Float(string='HG', readonly=1, compute="_compute_percent_back", store=True)

    KG = fields.Integer(string='KG (Tờ)')
    KG_PC = fields.Float(string='KG', readonly=1, compute="_compute_percent_back", store=True)

    DL = fields.Integer(string='ĐL (Tờ)')
    DL_PC = fields.Float(string='ĐL', readonly=1, compute="_compute_percent_back", store=True)

    TG = fields.Integer(string='TG (Tờ)')
    TG_PC = fields.Float(string='TG', readonly=1, compute="_compute_percent_back", store=True)

    percent = fields.Float("%", compute="_compute_percent", store=True)
    sum_return = fields.Integer("Tổng trả (Tờ)", compute="_compute_sum_return", store=True)
    consume = fields.Integer("Tiêu thụ", compute="_compute_consume", store=True)
    ticket_receive = fields.Integer("Lượng vé lãnh", compute='_compute_ticket_receive', store=True)
    du_thieu = fields.Integer('Dư thiếu')
    revenues = fields.Integer('Tiền thu', compute="_compute_revenues", store=True)
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
                [('planed_id.date', '=', r.return_stock_id.date), ('customer_id', '=', r.customer_id.id)])
            total = sum(plan.mapped('total'))
            r.consume = total - r.sum_return * 10000

    @api.depends('return_stock_id', 'return_stock_id.day_of_week')
    def _compute_ticket_receive(self):
        for r in self:
            customer_plan = self.env['customer.plan'].get_val_customer_plan()
            day_week = customer_plan.get(r.customer_id.planed.code)

            if day_week == 0:
                r.ticket_receive = (r.customer_id.HCM + r.customer_id.DT + r.customer_id.CM)
            elif day_week == 1:
                r.ticket_receive = (r.customer_id.BL + r.customer_id.BT + r.customer_id.VT)
            elif day_week == 2:
                r.ticket_receive = (r.customer_id.ST + r.customer_id.CT + r.customer_id.DN)
            elif day_week == 3:
                r.ticket_receive = (r.customer_id.TN + r.customer_id.AG + r.customer_id.BTH)
            elif day_week == 4:
                r.ticket_receive = (r.customer_id.BD + r.customer_id.TV + r.customer_id.VL)
            elif day_week == 5:
                r.ticket_receive = (r.customer_id.HCM_2 + r.customer_id.LA + r.customer_id.BP + r.customer_id.HG)
            elif day_week == 6:
                r.ticket_receive = (r.customer_id.KG + r.customer_id.DL + r.customer_id.TG)

    @api.depends('ticket_receive', 'sum_return', 'du_thieu')
    def _compute_revenues(self):
        for r in self:
            planed_main = self.env['planed.line'].search(
                [('planed_id.date', '=', r.return_stock_id.date), ('customer_id', '=', r.customer_id.id)])
            p1, p2, p3, p4 = 0, 0, 0, 0
            customer_plan = self.env['customer.plan'].get_val_customer_plan()
            day_week = customer_plan.get(r.customer_id.planed.code)
            if planed_main.planed_id.day_of_week == '0':
                p1 = (planed_main.HCM + planed_main.HCM_PS) * r.customer_id.HCM_price
                p2 = (planed_main.DT + planed_main.DT_PS) * r.customer_id.DT_price
                p3 = (planed_main.CM + planed_main.CM_PS) * r.customer_id.CM_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 2:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.CT + plan.CT_PS) * r.customer_id.BT_price
                    p3 = (plan.DN + plan.DN_PS) * r.customer_id.DN_price
                elif day_week == 3:
                    p1 = (plan.TN + plan.TN_PS) * r.customer_id.TN_price
                    p2 = (plan.AG + plan.AG_PS) * r.customer_id.AG_price
                    p3 = (plan.BTH + plan.BTH_PS) * r.customer_id.BTH_price
                elif day_week == 4:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price
                elif day_week == 5:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price
                elif day_week == 6:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                p1 = p1 - ((r.HCM * 10000) * r.customer_id.HCM_price)
                p2 = p2 - ((r.DT * 10000) * r.customer_id.DT_price)
                p3 = p3 - ((r.CM * 10000) * r.customer_id.CM_price)
            if planed_main.planed_id.day_of_week == '1':
                p1 = (planed_main.BL + planed_main.BL_PS) * r.customer_id.BL_price
                p2 = (planed_main.BT + planed_main.BT_PS) * r.customer_id.BT_price
                p3 = (planed_main.VT + planed_main.VT_PS) * r.customer_id.VT_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.CT + plan.CT_PS) * r.customer_id.CT_price
                    p3 = (plan.DN + plan.DN_PS) * r.customer_id.DN_price
                elif day_week == 2:
                    p1 = (plan.TN + plan.TN_PS) * r.customer_id.TN_price
                    p2 = (plan.AG + plan.AG_PS) * r.customer_id.AG_price
                    p3 = (plan.BTH + plan.BTH_PS) * r.customer_id.BTH_price
                elif day_week == 3:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price
                elif day_week == 4:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price
                elif day_week == 5:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                elif day_week == 6:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price

                p1 = p1 - ((r.BL * 10000) * r.customer_id.BL_price)
                p2 = p2 - ((r.BT * 10000) * r.customer_id.BT_price)
                p3 = p3 - ((r.VT * 10000) * r.customer_id.VT_price)
            if planed_main.planed_id.day_of_week == '2':
                p1 = (planed_main.ST + planed_main.ST_PS) * r.customer_id.ST_price
                p2 = (planed_main.CT + planed_main.CT_PS) * r.customer_id.CT_price
                p3 = (planed_main.DN + planed_main.DN_PS) * r.customer_id.DN_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.TN + plan.TN_PS) * r.customer_id.TN_price
                    p2 = (plan.AG + plan.AG_PS) * r.customer_id.AG_price
                    p3 = (plan.BTH + plan.BTH_PS) * r.customer_id.BTH_price
                elif day_week == 2:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price
                elif day_week == 3:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price
                elif day_week == 4:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                elif day_week == 5:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price
                elif day_week == 6:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price

                p1 = p1 - ((r.ST * 10000) * r.customer_id.ST_price)
                p2 = p2 - ((r.CT * 10000) * r.customer_id.CT_price)
                p3 = p3 - ((r.DN * 10000) * r.customer_id.DN_price)
            if planed_main.planed_id.day_of_week == '3':
                p1 = (planed_main.TN + planed_main.TN_PS) * r.customer_id.TN_price
                p2 = (planed_main.AG + planed_main.AG_PS) * r.customer_id.AG_price
                p3 = (planed_main.BTH + planed_main.BTH_PS) * r.customer_id.BTH_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price
                elif day_week == 2:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price
                elif day_week == 3:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                elif day_week == 4:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price
                elif day_week == 5:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 6:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price

                p1 = p1 - ((r.TN * 10000) * r.customer_id.TN_price)
                p2 = p2 - ((r.AG * 10000) * r.customer_id.AG_price)
                p3 = p3 - ((r.BTH * 10000) * r.customer_id.BTH_price)
            if planed_main.planed_id.day_of_week == '4':
                p1 = (planed_main.BD + planed_main.BD_PS) * r.customer_id.BD_price
                p2 = (planed_main.TV + planed_main.TV_PS) * r.customer_id.TV_price
                p3 = (planed_main.VL + planed_main.VL_PS) * r.customer_id.VL_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price
                elif day_week == 2:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                elif day_week == 3:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price
                elif day_week == 4:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 5:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 6:
                    p1 = (plan.TN + plan.TN_PS) * r.customer_id.TN_price
                    p2 = (plan.AG + plan.AG_PS) * r.customer_id.AG_price
                    p3 = (plan.BTH + plan.BTH_PS) * r.customer_id.BTH_price

                p1 = p1 - ((r.BD * 10000) * r.customer_id.BD_price)
                p2 = p2 - ((r.TV * 10000) * r.customer_id.TV_price)
                p3 = p3 - ((r.VL * 10000) * r.customer_id.VL_price)
            if planed_main.planed_id.day_of_week == '5':
                p1 = (planed_main.HCM_2 + planed_main.HCM_2_PS) * r.customer_id.HCM_2_price
                p2 = (planed_main.LA + planed_main.LA_PS) * r.customer_id.LA_price
                p3 = (planed_main.BP + planed_main.BP_PS) * r.customer_id.BP_price
                p4 = (planed_main.HG + planed_main.HG_PS) * r.customer_id.HG_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.KG + plan.KG_PS) * r.customer_id.KG_price
                    p2 = (plan.DL + plan.DL_PS) * r.customer_id.DL_price
                    p3 = (plan.TG + plan.TG_PS) * r.customer_id.TG_price
                elif day_week == 2:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price
                elif day_week == 3:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 4:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 5:
                    p1 = (plan.TN + plan.TN_PS) * r.customer_id.TN_price
                    p2 = (plan.AG + plan.AG_PS) * r.customer_id.AG_price
                    p3 = (plan.BTH + plan.BTH_PS) * r.customer_id.BTH_price
                elif day_week == 6:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price

                p1 = p1 - ((r.HCM_2 * 10000) * r.customer_id.HCM_2_price)
                p2 = p2 - ((r.LA * 10000) * r.customer_id.LA_price)
                p3 = p3 - ((r.BP * 10000) * r.customer_id.BP_price)
                p4 = p4 - ((r.HG * 10000) * r.customer_id.HG_price)
            if planed_main.planed_id.day_of_week == '6':
                p1 = (planed_main.KG + planed_main.KG_PS) * r.customer_id.KG_price
                p2 = (planed_main.DL + planed_main.DL_PS) * r.customer_id.DL_price
                p3 = (planed_main.TG + planed_main.TG_PS) * r.customer_id.TG_price
                if day_week != 0:
                    plan = self.env['planed.line'].search(
                        [('planed_id.date', '=', r.return_stock_id.date + timedelta(days=day_week)),
                         ('customer_id', '=', r.customer_id.id)])
                else:
                    plan = planed_main
                if day_week == 1:
                    p1 = (plan.HCM + plan.HCM_PS) * r.customer_id.HCM_price
                    p2 = (plan.DT + plan.DT_PS) * r.customer_id.DT_price
                    p3 = (plan.CM + plan.CM_PS) * r.customer_id.CM_price
                elif day_week == 2:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 3:
                    p1 = (plan.BL + plan.BL_PS) * r.customer_id.BL_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 4:
                    p1 = (plan.ST + plan.ST_PS) * r.customer_id.ST_price
                    p2 = (plan.BT + plan.BT_PS) * r.customer_id.BT_price
                    p3 = (plan.VT + plan.VT_PS) * r.customer_id.VT_price
                elif day_week == 5:
                    p1 = (plan.BD + plan.BD_PS) * r.customer_id.BD_price
                    p2 = (plan.TV + plan.TV_PS) * r.customer_id.TV_price
                    p3 = (plan.VL + plan.VL_PS) * r.customer_id.VL_price
                elif day_week == 6:
                    p1 = (plan.HCM_2 + plan.HCM_2_PS) * r.customer_id.HCM_2_price
                    p2 = (plan.LA + plan.LA_PS) * r.customer_id.LA_price
                    p3 = (plan.BP + plan.BP_PS) * r.customer_id.BP_price
                    p4 = (plan.HG + plan.HG_PS) * r.customer_id.HG_price

                p1 = p1 - ((r.KG * 10000) * r.customer_id.KG_price)
                p2 = p2 - ((r.DL * 10000) * r.customer_id.DL_price)
                p3 = p3 - ((r.TG * 10000) * r.customer_id.TG_price)
            r.revenues = (p1 + p2 + p3 + p4)

    @api.depends('HCM', 'DT', 'CM', 'BL', 'BT', 'VT', 'ST', 'CT', 'DN', 'TN', 'AG',
                 'BTH', 'BD', 'TV', 'VL', 'HCM_2', 'LA', 'BP', 'HG', 'KG', 'DL', 'TG')
    def _compute_percent_back(self):
        for r in self:
            planed = self.env['planed.line'].search([('planed_id.date', '=', r.return_stock_id.date), ('customer_id', '=', r.customer_id.id)], limit=1)
            r.HCM_PC = ((r.HCM * 10000) / (r.customer_id.HCM + planed.HCM_PS)) * 100 if r.customer_id.HCM > 0 else 0
            r.DT_PC = ((r.DT * 10000) / (r.customer_id.DT + planed.DT_PS)) * 100 if r.customer_id.DT > 0 or planed.DT_PS > 0 else 0
            r.CM_PC = ((r.CM * 10000) / (r.customer_id.CM + planed.CM_PS)) * 100 if r.customer_id.CM > 0 or planed.CM_PS > 0 else 0
            r.BL_PC = ((r.BL * 10000) / (r.customer_id.BL + planed.BL_PS)) * 100 if r.customer_id.BL > 0 or planed.BL_PS > 0 else 0
            r.BT_PC = ((r.BT * 10000) / (r.customer_id.BT + planed.BT_PS)) * 100 if r.customer_id.BT > 0 or planed.BT_PS > 0 else 0
            r.VT_PC = ((r.VT * 10000) / (r.customer_id.VT + planed.VT_PS)) * 100 if r.customer_id.VT > 0 or planed.VT_PS > 0 else 0
            r.ST_PC = ((r.ST * 10000) / (r.customer_id.ST + planed.ST_PS)) * 100 if r.customer_id.ST > 0 or planed.ST_PS > 0 else 0
            r.CT_PC = ((r.CT * 10000) / (r.customer_id.CT + planed.CT_PS)) * 100 if r.customer_id.CT > 0 or planed.CT_PS > 0 else 0
            r.DN_PC = ((r.DN * 10000) / (r.customer_id.DN + planed.DN_PS)) * 100 if r.customer_id.DN > 0 or planed.DN_PS > 0 else 0
            r.TN_PC = ((r.TN * 10000) / (r.customer_id.TN + planed.TN_PS)) * 100 if r.customer_id.TN > 0 or planed.TN_PS > 0 else 0
            r.AG_PC = ((r.AG * 10000) / (r.customer_id.AG + planed.AG_PS)) * 100 if r.customer_id.AG > 0 or planed.AG_PS > 0 else 0
            r.BTH_PC = ((r.BTH * 10000) / (r.customer_id.BTH + planed.BTH_PS)) * 100 if r.customer_id.BTH > 0 or planed.BTH_PS > 0 else 0
            r.BD_PC = ((r.BD * 10000) / (r.customer_id.BD + planed.BD_PS)) * 100 if r.customer_id.BD > 0 or planed.BD_PS > 0 else 0
            r.TV_PC = ((r.TV * 10000) / (r.customer_id.TV + planed.TV_PS)) * 100 if r.customer_id.TV > 0 or planed.TV_PS > 0 else 0
            r.VL_PC = ((r.VL * 10000) / (r.customer_id.VL + planed.VL_PS)) * 100 if r.customer_id.VL > 0 or planed.VL_PS > 0 else 0
            r.HCM_2_PC = ((r.HCM_2 * 10000) / (r.customer_id.HCM_2 + planed.HCM_2_PS)) * 100 if r.customer_id.HCM_2 > 0 or planed.HCM_2_PS > 0 else 0
            r.LA_PC = ((r.LA * 10000) / (r.customer_id.LA + planed.LA_PS)) * 100 if r.customer_id.LA > 0 or planed.LA_PS > 0 else 0
            r.BP_PC = ((r.BP * 10000) / (r.customer_id.BP + planed.BP_PS)) * 100 if r.customer_id.BP > 0 or planed.BP_PS > 0 else 0
            r.HG_PC = ((r.HG * 10000) / (r.customer_id.HG + planed.HG_PS)) * 100 if r.customer_id.HG > 0 or planed.HG_PS > 0 else 0
            r.KG_PC = ((r.KG * 10000) / (r.customer_id.KG + planed.KG_PS)) * 100 if r.customer_id.KG > 0 or planed.KG_PS > 0 else 0
            r.DL_PC = ((r.DL * 10000) / (r.customer_id.DL + planed.DL_PS)) * 100 if r.customer_id.DL > 0 or planed.DL_PS > 0 else 0
            r.TG_PC = ((r.TG * 10000) / (r.customer_id.TG + planed.TG_PS)) * 100 if r.customer_id.TG > 0 or planed.TG_PS > 0 else 0

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
    BL = fields.Char(string='BL', compute="_compute_tele_value")
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
                r.HCM = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HCM')))
                r.DT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DT')))
                r.CM = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('CM')))
                r.BL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BL')))
                r.BT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BT')))
                r.VT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('VT')))
                r.ST = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('ST')))
                r.CT = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('CT')))
                r.DN = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DN')))
                r.TN = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TN')))
                r.AG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('AG')))
                r.BTH = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BTH')))
                r.BD = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BD')))
                r.TV = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TV')))
                r.VL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('VL')))
                r.HCM_2 = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HCM_2')))
                r.LA = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('LA')))
                r.BP = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('BP')))
                r.HG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('HG')))
                r.KG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('KG')))
                r.DL = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('DL')))
                r.TG = "{:,.0f}".format(sum(r.return_stock_id.lines.mapped('TG')))
            elif r.data_tele_id.code == 'tl':
                quantities = self.env['purchase.inventory'].get_total(date=self.return_stock_id.date)
                r.HCM = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('HCM')) * 10000 / quantities['HCM_1']) * 100) if quantities.get('HCM_1', 0)>0 else 0)
                r.DT = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('DT')) * 10000 / quantities['DT']) * 100) if quantities.get('DT', 0)>0 else 0)
                r.CM = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('CM')) * 10000 / quantities['CM']) * 100) if quantities.get('CM', 0)>0 else 0)
                r.BL = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('BL')) * 10000 / quantities['BL']) * 100) if quantities.get('BL', 0)>0 else 0)
                r.BT = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('BT')) * 10000 / quantities['BT']) * 100) if quantities.get('BT', 0)>0 else 0)
                r.VT = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('VT')) * 10000 / quantities['VT']) * 100) if quantities.get('VT', 0)>0 else 0)
                r.ST = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('ST')) * 10000 / quantities['ST']) * 100) if quantities.get('ST', 0)>0 else 0)
                r.CT = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('CT')) * 10000 / quantities['CT']) * 100) if quantities.get('CT', 0)>0 else 0)
                r.DN = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('DN')) * 10000 / quantities['DN']) * 100) if quantities.get('DN', 0)>0 else 0)
                r.TN = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('TN')) * 10000 / quantities['TN']) * 100) if quantities.get('TN', 0)>0 else 0)
                r.AG = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('AG')) * 10000 / quantities['AG']) * 100) if quantities.get('AG', 0)>0 else 0)
                r.BTH = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('BTH')) * 10000 / quantities['BTH']) * 100) if quantities.get('BTH', 0)>0 else 0)
                r.BD = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('BD')) * 10000 / quantities['BD']) * 100) if quantities.get('BD', 0)>0 else 0)
                r.TV = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('TV')) * 10000 / quantities['TV']) * 100) if quantities.get('TV', 0)>0 else 0)
                r.VL = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('VL')) * 10000 / quantities['VL']) * 100) if quantities.get('VL', 0)>0 else 0)
                r.HCM_2 = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('HCM_2')) * 10000 / quantities['HCM_2']) * 100) if quantities.get('HCM_2', 0)>0 else 0)
                r.LA = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('LA')) * 10000 / quantities['LA']) * 100) if quantities.get('LA', 0)>0 else 0)
                r.BP = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('BP')) * 10000 / quantities['BP']) * 100) if quantities.get('BP', 0)>0 else 0)
                r.HG = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('HG')) * 10000 / quantities['HG']) * 100) if quantities.get('HG', 0)>0 else 0)
                r.KG = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('KG')) * 10000 / quantities['KG']) * 100) if quantities.get('KG', 0)>0 else 0)
                r.DL = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('DL')) * 10000 / quantities['DL']) * 100) if quantities.get('DL', 0)>0 else 0)
                r.TG = "{:,.3f}%".format(((sum(r.return_stock_id.lines.mapped('TG')) * 10000 / quantities['TG']) * 100) if quantities.get('TG', 0)>0 else 0)
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
