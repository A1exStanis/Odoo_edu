from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class DoctorDiseaseReportWizard(models.TransientModel):
    _name = 'doctor.disease.report.wizard'
    _description = 'Doctor Disease Report Wizard'

    year = fields.Integer(string='Year', required=True)
    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], string='Month', required=True)

    def action_generate_report(self):
        year = int(self.year)
        month = int(self.month)

        start_date = f'{year}-{month:02d}-01'
        end_date = f'{year}-{month:02d}-{self._days_in_month(year, month):02d}'

        diagnoses = self.env['hospital.diagnosis'].search([
            ('diagnosis_date', '>=', start_date),
            ('diagnosis_date', '<=', end_date)
        ])

        disease_counts = {}
        for diag in diagnoses:
            name = diag.disease_id.name
            if name not in disease_counts:
                disease_counts[name] = 0
            disease_counts[name] += 1

        report_data = {
            'year': year,
            'month': month,
            'disease_ids': [{'disease_id': {'name': name}, 'count': count} for name, count in disease_counts.items()]
        }

        return self.env.ref('hospital.report_disease_report').report_action(self, data={'doc': report_data})

    def _days_in_month(self, year, month):
        import calendar
        return calendar.monthrange(year, month)[1]