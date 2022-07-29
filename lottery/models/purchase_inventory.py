from odoo import fields, api, models
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError


class PurchaseInventory(models.Model):
    _name = 'purchase.inventory'

    @api.model
    def default_get(self, fields_list):
        res = super(PurchaseInventory, self).default_get(fields_list)
        province_ids = self.env['province.lottery'].search([('group', '=', self._context.get('default_day_of_week'))])
        val_lines = []
        for p in province_ids:
            val_lines.append((0, 0, {'province_id': p.id}))
        res.update({'lines': val_lines})
        return res

    name = fields.Char('Tên phiếu nhập')
    date = fields.Date('Ngày nhập', default=datetime.now(), readonly=1)
    lines = fields.One2many('purchase.inventory.line', 'purchase_id', string='Chi tiết')
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

    def unlink(self):
        for rec in self:
            if rec.state == 'done':
                raise ValidationError('Không thể xóa phiếu nhập kho đã hoàn thành')
        return super(PurchaseInventory, self).unlink()

    def get_total(self, date):
        inventory = self.search([('date', '=', date)], limit=1)
        vals = {}
        for item in inventory.lines:
            vals.update({
                item.province_id.code: item.total
            })
        return vals

    def cron_create_inventory(self):
        # old = self.search([('date', '=', datetime.now() - timedelta(days=1))], limit=1, order='id desc')
        from datetime import date
        current = self.search([('date', '=', date.today())], limit=1, order='id desc')
        if not current:
            return False
        exists = self.search([('date', '=', (date.today() + timedelta(weeks=1)))], limit=1, order='id desc')
        if exists:
            return False
        val_lines = []
        for line in current.lines:
            val_lines.append((0, 0, {
                'province_id': line.province_id.id,
                'in_company': line.in_company,
                'in_province': line.in_province,
                'total': line.total,
            }))
        create_date = (date.today() + timedelta(weeks=1))
        self.create({
            'name': f"Nhập kho ngày: {create_date}",
            'date': create_date,
            'lines': val_lines
        })
        return True


class PurchaseInventoryLine(models.Model):
    _name = 'purchase.inventory.line'

    purchase_id = fields.Many2one('purchase.inventory', string='Phiếu nhập kho')
    province_id = fields.Many2one('province.lottery', string='Tên đài', readonly=1)
    in_company = fields.Integer(string='Số lượng nhập (Công ty)')
    in_province = fields.Integer(string='Số lượng nhập (Liên tỉnh)')
    total = fields.Integer(string='Tổng số nhập', compute='_compute_total')

    @api.depends('in_company', 'in_province')
    def _compute_total(self):
        for item in self:
            item.total = (item.in_company + item.in_province)


class ProvinceLottery(models.Model):
    _name = 'province.lottery'

    name = fields.Char(string='Tên đài')
    code = fields.Char(string='Mã đài', readonly=1)
    group = fields.Selection([
        ('0', 'Thứ 2'),
        ('1', 'Thứ 3'),
        ('2', 'Thứ 4'),
        ('3', 'Thứ 5'),
        ('4', 'Thứ 6'),
        ('5', 'Thứ 7'),
        ('6', 'Chủ nhật')
    ], string='Ngày quay')