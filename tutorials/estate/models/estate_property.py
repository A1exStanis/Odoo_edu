from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Data for estate properties'

    name = fields.Char('Estate name', required=True)
    description = fields.Text('Estate description')
    postcode = fields.Char('Zip code', default=None)
    data_availability = fields.Date('When is available')
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float('Selling price')
    bedrooms = fields.Integer('Number of bedrooms')
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage', default=False)
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east', 'East'),
                   ('west', 'West')])
