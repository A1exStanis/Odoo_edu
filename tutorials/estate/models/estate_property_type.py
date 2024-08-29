from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char('Estate Type', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1)
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_type_id',
        string='Offers'
    )
    offer_count = fields.Integer(
        string='Number of Offers',
        compute='_compute_offer_count',
        store=True
    )

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name of the property type must be unique.')
    ]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

