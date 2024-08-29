from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char('Estate Tag', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The name of the property tag must be unique.')
    ]