from odoo import models, fields


class SampleType(models.Model):
    _name = 'sample.type'
    _description = 'Sample Type'

    name = fields.Char(string='Type Name', required=True)

