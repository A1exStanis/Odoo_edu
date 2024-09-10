from odoo import models, fields


class ResearchDirectory(models.Model):
    _name = 'research.directory'
    _description = 'Research Directory'

    name = fields.Char(string='Research Name', required=True)
    description = fields.Text(string='Description')
    research_type_id = fields.Many2one('research.type', string='Disease Type', required=True)
    sample_type_id = fields.Many2one('sample.type', string='Sample Type')
    diagnosis_id = fields.Many2one('hospital.diagnosis', string='Diagnosis')
    visit_id = fields.Many2one('doctor.visit', string='Doctor Visit')