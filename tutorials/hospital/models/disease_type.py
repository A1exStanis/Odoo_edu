from odoo import models, fields


class DiseaseType(models.Model):
    _name = 'disease.type'
    _description = 'Disease Type'

    name = fields.Char(string='Type Name', required=True)
    disease_directory_ids = fields.One2many('disease.directory', 'disease_type_id',
                                            string='Disease Directories')
    description = fields.Text(string='Description')
