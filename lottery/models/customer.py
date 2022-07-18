from odoo import fields, api, models


class Customer(models.Model):
    _name = 'customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
                                 string='Related Partner', help='Partner-related data of the user')
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False, required=1, string='Họ tên', tracking=True)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False, tracking=True)
    gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')],
                              string='Giới tính',
                              default='nam', tracking=True)
    phone = fields.Char(string='Số điện thoại', required=1, tracking=True)
    address = fields.Char(string='Địa chỉ', required=1, tracking=True)
    status = fields.Selection([('active', 'Hoạt động'), ('locked', 'Khóa')],
                              string='Trạng thái',
                              default='active', tracking=True)
    note = fields.Char(string='Ghi chú', tracking=True)
    planed = fields.Many2one('customer.plan', string='Kế hoạch lãnh', required=1, tracking=True)

    HCM = fields.Integer(string='TP HCM', tracking=True)
    DT = fields.Integer(string='ĐT', tracking=True)
    CM = fields.Integer(string='CM', tracking=True)
    BL = fields.Integer(string='CM', tracking=True)
    BT = fields.Integer(string='BT', tracking=True)
    VT = fields.Integer(string='VT', tracking=True)
    ST = fields.Integer(string='ST', tracking=True)
    CT = fields.Integer(string='ST', tracking=True)
    DN = fields.Integer(string='ĐN', tracking=True)
    TN = fields.Integer(string='TN', tracking=True)
    AG = fields.Integer(string='AG', tracking=True)
    BTH = fields.Integer(string='BTH', tracking=True)
    BD = fields.Integer(string='BD', tracking=True)
    TV = fields.Integer(string='TV', tracking=True)
    VL = fields.Integer(string='VL', tracking=True)
    HCM_2 = fields.Integer(string='TP HCM', tracking=True)
    LA = fields.Integer(string='LA', tracking=True)
    BP = fields.Integer(string='BP', tracking=True)
    HG = fields.Integer(string='HG', tracking=True)
    KG = fields.Integer(string='KG', tracking=True)
    DL = fields.Integer(string='ĐL', tracking=True)
    TG = fields.Integer(string='TG', tracking=True)

    # đơn giá theo đài
    HCM_price = fields.Float(string='TP HCM', tracking=True, default=None, digits=(23, 4))
    DT_price = fields.Float(string='ĐT', tracking=True, digits=(23, 4))
    CM_price = fields.Float(string='CM', tracking=True, digits=(23, 4))
    BL_price = fields.Float(string='CM', tracking=True, digits=(23, 4))
    BT_price = fields.Float(string='BT', tracking=True, digits=(23, 4))
    VT_price = fields.Float(string='VT', tracking=True, digits=(23, 4))
    ST_price = fields.Float(string='ST', tracking=True, digits=(23, 4))
    CT_price = fields.Float(string='ST', tracking=True, digits=(23, 4))
    DN_price = fields.Float(string='ĐN', tracking=True, digits=(23, 4))
    TN_price = fields.Float(string='TN', tracking=True, digits=(23, 4))
    AG_price = fields.Float(string='AG', tracking=True, digits=(23, 4))
    BTH_price = fields.Float(string='BTH', tracking=True, digits=(23, 4))
    BD_price = fields.Float(string='BD', tracking=True, digits=(23, 4))
    TV_price = fields.Float(string='TV', tracking=True, digits=(23, 4))
    VL_price = fields.Float(string='VL', tracking=True, digits=(23, 4))
    HCM_2_price = fields.Float(string='TP HCM', tracking=True, digits=(23, 4))
    LA_price = fields.Float(string='LA', tracking=True, digits=(23, 4))
    BP_price = fields.Float(string='BP', tracking=True, digits=(23, 4))
    HG_price = fields.Float(string='HG', tracking=True, digits=(23, 4))
    KG_price = fields.Float(string='KG', tracking=True, digits=(23, 4))
    DL_price = fields.Float(string='ĐL', tracking=True, digits=(23, 4))
    TG_price = fields.Float(string='TG', tracking=True, digits=(23, 4))

    def create_customer(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


class CustomerPlan(models.Model):
    _name = 'customer.plan'

    name = fields.Char('Tên kế hoạch')
    code = fields.Char('Mã kế hoạch')
    state = fields.Selection([('active', 'Hoạt động'), ('inactive', 'Ngừng hoạt động')])

    def get_val_customer_plan(self):
        customer_plan = self.env['customer.plan'].search([])
        vals = {}
        num = 0
        for p in customer_plan:
            if num == 7:
                break
            vals.update({
                p.code : num
            })
            num += 1
        return vals