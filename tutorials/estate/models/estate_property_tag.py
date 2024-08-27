from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char('Estate Tag', required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name of the property tag must be unique.')
    ]