from odoo import models, fields


class DiseaseDirectory(models.Model):
    _name = 'disease.directory'
    _description = 'Disease Directory'

    name = fields.Char(string='Disease Name', required=True)
    description = fields.Text(string='Description')
    disease_type_id = fields.Many2one('disease.type', string='Disease Type', required=True)
    