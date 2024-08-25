from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('refused', 'Refused'),
                   ('accepted', 'Accepted')],
        default=None)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'price': self.price
        })
        return super(EstatePropertyOffer, self).copy(default)

