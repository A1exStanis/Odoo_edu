from odoo import models, fields


class SpecialtyType(models.Model):
    _name = 'specialty.type'
    _description = 'Specialty type for doctors'

    name = fields.Char(string='Specialty Name', required=True)