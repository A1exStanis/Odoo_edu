from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price DESC'

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('refused', 'Refused'),
                   ('accepted', 'Accepted')],
        default=None)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Date Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type',
                                       related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.context_today(record) + timedelta(days=record.validity)

    @api.onchange('validity', 'create_date')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.context_today(record) + timedelta(days=record.validity)

    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'price': self.price
        })
        return super(EstatePropertyOffer, self).copy(default)

    def action_accept(self):
        if self.status == 'accepted':
            raise UserError('This offer is already accepted.')
        if self.status == 'refused':
            raise UserError('Cannot accept a refused offer.')
        self.write({'status': 'accepted'})
        self.property_id.write({
            'state': 'offer_accepted',
            'buyer_id': self.partner_id.id,
            'selling_price': self.price
        })

    def action_refuse(self):
        if self.status == 'refused':
            raise UserError('This offer is already refused.')
        if self.status == 'accepted':
            raise UserError('Cannot refuse an accepted offer.')
        self.write({'status': 'refused'})
