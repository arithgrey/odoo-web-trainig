
from odoo.exceptions import UserError
from odoo import models, api, fields, _
from datetime import timedelta


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    pos_order_id = fields.Many2one('pos.order', 'Pos Order')


class PosOrderInherit(models.Model):
    _name = 'pos.order'
    _inherit = ['pos.order',
                'portal.mixin',
                'mail.thread',
                'mail.activity.mixin']
    _description = "Point of Sale Orders"
    _order = "id desc"

    lines = fields.One2many('pos.order.line', 'order_id', readonly=False)
    picking_ids = fields.One2many(
        'stock.picking', 'pos_order_id', string='Pickings')
    partner_invoice_id = fields.Many2one('res.partner')
    delivery_count = fields.Integer(
        string='Delivery Orders', compute='_compute_picking_ids')
    bnf_partner_shipping_id = fields.Many2one('res.partner')
    invoice_address_type = fields.Selection([
        ('same', 'Same'),
        ('other', 'Other')
    ])
    ticket_url = fields.Char()
    bnf_shipping_type = fields.Selection([
        ('home', 'Home'),
        ('temple', 'Temple'),
        ('right_now', 'Right now')
    ])
    manufacturing_count = fields.Integer(
        string='Manufacturing Orders',
        compute='_compute_manufacturing_count')
    prescription_count = fields.Integer(
        string='Prescriptions',
        compute='_compute_prescription_count')
    cancel_message = fields.Char(
        help='Message used to identify if an order was canceled')

    @api.multi
    def refund(self):
        """Added a relation between the refund order and the original one"""
        res = super(PosOrderInherit, self).refund()
        if not res.get('res_id'):
            return res
        note_id = self.env.ref('mail.mt_note').id
        origin = self[0]
        refund = self.browse(res['res_id'])
        refund.message_post_with_view(
            'mail.message_origin_link',
            values={'self': refund, 'origin': origin},
            subtype_id=note_id)
        origin.message_post_with_view(
            'mail.message_origin_link',
            values={'self': origin, 'origin': refund, 'edit': True},
            subtype_id=note_id)
        try:
            mrp = self.env['mrp.production'].search([
                ('pos_order_id', '=', origin.id),
                ('state', 'in', ('confirmed', 'planned', 'progress'))])
            mrp.post_inventory()
            mrp.action_cancel()
            origin.picking_ids.action_cancel()
        except BaseException:
            message = _('There was an error when we tried to cancel the stock '
                        'moves related with this order, please check the '
                        'orders and leave a message '
                        'when you have done')
            (origin + refund).write({'cancel_message': message})
        return res

    @api.multi
    def action_cancel(self):
        """Cancel inventory moves related with this order"""
        mrp_obj = self.env['mrp.production']
        for rec in self:
            try:
                mrp = mrp_obj.search([('pos_order_id', '=', rec.id)])
                mrp.action_cancel()
                rec.picking_ids.action_cancel()
            except BaseException as err:
                raise UserError(
                    _('We cannot cancel this order automatically because %s.'
                      ' \n Please check the process and cancel it manually') %
                    err)
        self.write({'cancel_message': _('Canceled')})

    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for order in self:
            order.delivery_count = len(order.picking_ids)

    @api.depends('lines')
    def _compute_manufacturing_count(self):
        mrp = self.env['mrp.production'].sudo()
        for order in self:
            order.manufacturing_count = mrp.search_count(
                [('pos_order_id', '=', order.id)])

    @api.multi
    def _compute_prescription_count(self):
        for order in self:
            order.prescription_count = len(order.mapped(
                'lines.prescription_id'))

    @api.multi
    def action_view_delivery(self):
        """This function returns an action that display existing delivery
        orders of given sales order ids. It can either be a in a list or
        in a form view, if there is only one delivery order to show.
        """
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        pickings = self.mapped('picking_ids')
        action['domain'] = [('id', 'in', pickings.ids)]
        return action

    @api.model
    def _process_order(self, pos_order):
        orders = super()._process_order(pos_order)
        for order in orders:
            order.set_warehouse()
            order.lines._action_launch_stock_rule()
            order.lines.send_prescription_attachment()
        return orders

    def create_picking(self):
        """This method is useless because we are using stock rules here. Yes,
        stock rules, sorry for this"""
        pickings = self.env['stock.picking'].search(
            [('pos_order_id', '=', self.id)])
        if not pickings or len(pickings) > 1:
            return True
        picking = pickings.filtered(
            lambda a: a.state in ('confirmed', 'assigned'))
        if not pickings:
            return True
        picking.action_assign()
        wrong_lots = self.set_pack_operation_lot(picking)
        if not wrong_lots:
            picking.action_done()
        return True

    @api.model
    def _order_fields(self, ui_order):
        """Sets the partner invoice and the temple for delivery depending
        in the order type.
        """
        values = super()._order_fields(ui_order)
        values['ticket_url'] = ui_order.get('ticket_url', False)
        values['note'] = ui_order.get('note', False)
        values['bnf_shipping_type'] = ui_order.get(
            'bnf_shipping_type', False)
        if ui_order.get('invoice_address_type') == 'other':
            values['partner_invoice_id'] = ui_order.get(
                'partner_invoice_id', False)
        else:
            values['partner_invoice_id'] = ui_order.get('partner_id')
        if values['bnf_shipping_type'] in ['temple', 'right_now']:
            values['bnf_partner_shipping_id'] = ui_order.get(
                'bnf_partner_shipping_id', False)
        return values

    @api.multi
    def set_warehouse(self):
        self.ensure_one()
        if self.bnf_shipping_type not in ['temple', 'right_now']:
            return
        warehouse_id = self.env['stock.warehouse'].search([
            ('partner_id', '=', self.bnf_partner_shipping_id.id)
        ], limit=1)
        if warehouse_id:
            self.warehouse_id = warehouse_id

    @api.model
    def _default_warehouse_id(self):
        company = self.env.user.company_id.id
        warehouse_ids = self.env['stock.warehouse'].search([
            ('company_id', '=', company)
        ], limit=1)
        return warehouse_ids

    helpdesk_id = fields.Many2one(
        'helpdesk.ticket',
        'RMA Ticket',
        help="RMA related with this order")

    commitment_date = fields.Datetime(
        states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
        copy=False, oldname='requested_date', readonly=True,
        help="""This is the delivery date promised to the customer. If set,
                the delivery order will be scheduled based on this date
                rather than product lead times.""")
    procurement_group_id = fields.Many2one(
        'procurement.group',
        'Procurement Group',
        copy=False)
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')],
        string='Shipping Policy', required=True,
        readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="""If you deliver all products at once, the delivery order will
                be scheduled based on the greatest product lead time.
                Otherwise, it will be based on the shortest.""")
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={
            'draft': [('readonly', False)],
            'sent': [('readonly', False)]
        },
        default=_default_warehouse_id)

    @api.multi
    def action_view_production(self):
        """This function returns an action that displays existing MO's
        of given pos order. It can either be a in a list or in a form
        view, if there is only one MO's in the order to show.
        """
        action = self.env.ref(
            'mrp.mrp_production_action').read()[0]
        mos = self.env['mrp.production'].sudo().search(
            [('pos_order_id', 'in', self._ids)])
        if len(mos) > 1:
            action['domain'] = [('id', 'in', mos.ids)]
        elif mos:
            action['views'] = [
                (self.env.ref(
                    'mrp.mrp_production_form_view').id,
                 'form')]
            action['res_id'] = mos.id
        return action

    def _action_create_invoice_line(self, line=False, invoice_id=False):
        inv_line = super(PosOrderInherit, self)._action_create_invoice_line(
            line, invoice_id)
        if not inv_line:
            return self.env['account.invoice.line']
        # Add discount if the invoice have a coupon applied
        if inv_line.price_unit <= 0:
            inv_line.write({
                'name': _('%s\nTotal Discount:%s\n') % (
                    inv_line.name,
                    inv_line.price_unit),
                'price_unit': 0,
            })
        lines = self.lines.filtered('qty')
        if inv_line.price_unit > 0 and lines.filtered(
                lambda line: line.price_subtotal <= 0):
            reward = lines.filtered(lambda line: line.price_subtotal <= 0)
            factor = abs(reward.price_subtotal) / sum((
                lines - reward).mapped('price_subtotal'))
            inv_line.write({
                'l10n_mx_edi_amount_discount': factor * inv_line.price_unit,
            })

        inv_line.name = inv_line.product_id.display_name
        percentage = self.company_id.benandfrank_split_percentage
        mica_prod = self.company_id.benandfrank_mica_product_id
        if percentage <= 0 or not mica_prod or percentage >= 100:
            return inv_line
        atts_mica = inv_line.product_id.attribute_value_ids.filtered(
            lambda x: x.attribute_id.widget_section in (
                'lens_color', 'graduation', 'antireflective', 'lens_material'))
        att_image_name = atts_mica.mapped('image_name')
        if not (inv_line.product_id and inv_line.product_id.is_spectacle
                ) or 'no_graduation' in att_image_name:
            return inv_line
        prod_tmpl = inv_line.product_id.product_tmpl_id
        line2 = inv_line.copy()
        discount = inv_line.l10n_mx_edi_amount_discount
        factor = discount / inv_line.price_unit
        line_price = self.pricelist_id.get_product_price(
            prod_tmpl, line.qty or 1.0, self.partner_id) * percentage / 100

        inv_line.write({
            'price_unit': line_price,
            'name': inv_line.product_id.name,
            'l10n_mx_edi_amount_discount': line_price * factor,
        })
        line_price = line2.price_unit - inv_line.price_unit
        line2.write({
            'price_unit': line2.price_unit - inv_line.price_unit,
            'product_id': mica_prod.id,
            'name': mica_prod.name + ' ' + ' '.join(atts_mica.mapped('name')),
            'l10n_mx_edi_amount_discount': line_price * factor,
        })
        return inv_line + line2

    @api.multi
    def get_date_order_delivery(self):

        date_order_delivery = self.date_order + timedelta(10)
        date_order_delivery_format = date_order_delivery.strftime("%d %b %Y")
        return date_order_delivery_format


class PosCategoryInherit(models.Model):

    _inherit = 'pos.category'

    is_template_category = fields.Boolean()