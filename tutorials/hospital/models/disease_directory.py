from odoo import models, fields, api
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class DiseaseDirectory(models.Model):
    _name = 'disease.directory'
    _description = 'Disease Directory'

    name = fields.Char(string='Disease Name', required=True)
    description = fields.Text(string='Description')
    disease_type_id = fields.Many2one('disease.type', string='Disease Type', required=True)
    diagnosis_ids = fields.One2many('hospital.diagnosis', 'disease_id', string='Diagnoses')

    @api.model
    def get_monthly_disease_report(self, year, month):
        start_date = f'{year}-{month}-01'
        end_date = (fields.Date.from_string(start_date) + relativedelta(months=1) - timedelta(days=1)).strftime(
            '%Y-%m-%d')

        diagnosis_data = self.env['hospital.diagnosis'].read_group(
            [('diagnosis_date', '>=', start_date), ('diagnosis_date', '<=', end_date)],
            ['disease_id', 'disease_id/name', 'disease_id/count'],
            ['disease_id']
        )
        return diagnosis_data