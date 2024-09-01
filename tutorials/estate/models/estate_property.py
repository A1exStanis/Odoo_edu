from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Data for estate properties'
    _order = 'id DESC'

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    data_availability = fields.Date('Available from',
                                    default=lambda self: self._default_date_due())
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'),
                   ('offer_receive', 'Offer Receive'),
                   ('offer_accepted', 'Offer Accepted'),
                   ('sold', 'Sold'),
                   ('canceled', 'Canceled')],
        default='new',
        required=True
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    seller_id = fields.Many2one('res.users', string='Seller', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tags_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Integer(string='Total Area (sqm)',
                                compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer',
                              compute='_compute_best_price')

    _sql_constraints = [
        ('expected_price_positive', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive'),
        ('selling_price_positive', 'CHECK(selling_price > 0)', 'Selling price must be positive')
    ]

    @api.model
    def create(self, vals):
        res = super(EstateProperty, self).create(vals)
        if 'offer_ids' in vals and vals['offer_ids']:
            res.state = 'offer_receive'
        return res

    @api.ondelete(at_uninstall=False)
    def _check_ondelete(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('Cannot delete property because it is not in a "New" or "Canceled" state.')

    @api.constrains('selling_price', 'expected_price')
    def _check_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and record.expected_price:
                if float_compare(record.selling_price, 0.9*record.expected_price, precision_digits=2) < 0:
                    raise UserError('The selling price cannot be lower than 90% of the expected price.')

    @api.onchange('garden')
    def _garden_onchange(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = False
                record.garden_orientation = False

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices, default=0.0)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _default_date_due(self):
        today = fields.Date.context_today(self)
        return today + relativedelta(months=3)

    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'state': 'new',
            'data_availability': self._default_date_due()
        })
        return super(EstateProperty, self).copy(default)

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError('Sold properties cannot be canceled ')
        self.write({"state": 'canceled'})

    def action_sold(self):
        if self.state == 'canceled':
            raise UserError('Canceled properties cannot be sold')
        self.write({'state': 'sold'})

    def action_offer_receive(self):
        self.write({'state': 'offer_receive'})

    def action_offer_accepted(self):
        self.write({'state': 'offer_accepted'})