from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Info about Diagnosis'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    disease_id = fields.Many2one('disease.directory', string='Disease')
    treatment = fields.Text(string='Treatment')
    diagnosis_date = fields.Date(string='Diagnosis date')
    mentor_comment = fields.Text(string='Mentor Comment')
    research_directory_ids = fields.One2many('research.directory', 'diagnosis_id', string='Researches')
    doctor_visit_id = fields.Many2one('doctor.visit', string='Doctor Vist')

    @api.constrains('doctor_id', 'mentor_comment')
    def _check_mentor_comment(self):
        for record in self:
            if record.doctor_id.is_intern and record.doctor_id.mentor_id:
                if not record.mentor_comment:
                    raise ValidationError("The mentor must provide a comment for diagnoses made by an intern.")