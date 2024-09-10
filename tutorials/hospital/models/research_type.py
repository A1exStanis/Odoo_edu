from odoo import models, fields


class ResearchType(models.Model):
    _name = 'research.type'
    _description = 'Research Type'

    name = fields.Char(string='Type Name', required=True)
    research_directory_ids = fields.One2many('research.directory', 'research_type_id',
                                             string='Research Directories')
    description = fields.Text(string='Description')

