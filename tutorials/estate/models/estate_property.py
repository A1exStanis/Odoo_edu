from odoo import models, fields
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Data for estate properties'

    name = fields.Char('Estate name', required=True)
    description = fields.Text('Estate description')
    postcode = fields.Char('Zip code')
    data_availability = fields.Date('When is available',
                                    default=lambda self: self._default_date_due())
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price', readonly=True)
    bedrooms = fields.Integer('Number of bedrooms', default=2)
    living_area = fields.Integer('Living area(sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden area(sqm)')
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
