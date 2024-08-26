from odoo import models, fields, api
from datetime import timedelta

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
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Date Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )

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

