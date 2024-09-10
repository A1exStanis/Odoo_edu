from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DoctorVisit(models.Model):
    _name = 'doctor.visit'
    _description = 'Doctor Visit'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    visit_date = fields.Date(string='Visit Date', required=True)
    visit_time = fields.Datetime(string='Visit Time', required=True)
    diagnosis_id = fields.Many2one('disease.directory', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    research_directory_ids = fields.Many2many('research.directory', string='Researches')
    appointment_confirmed = fields.Boolean(string='Appointment Confirmed', default=False)

    _sql_constraints = [
        ('unique_appointment', 'unique(doctor_id, visit_date, visit_time)',
         'An appointment already exists for this doctor at this time.')
    ]

    @api.constrains('visit_date', 'visit_time')
    def _check_visit_time(self):
        for record in self:
            if record.appointment_confirmed:
                raise ValidationError("You cannot change the date/time or doctor for a confirmed appointment.")

            overlapping_visits = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('visit_date', '=', record.visit_date),
                ('visit_time', '=', record.visit_time),
                ('id', '!=', record.id)
            ])
            if overlapping_visits:
                raise ValidationError("The doctor already has an appointment at this time.")

    @api.model
    def create(self, vals):
        if 'visit_time' in vals:
            existing_visit = self.search([
                ('doctor_id', '=', vals.get('doctor_id')),
                ('visit_date', '=', vals.get('visit_date')),
                ('visit_time', '=', vals.get('visit_time'))
            ])
            if existing_visit:
                raise ValidationError("An appointment already exists for this doctor at this time.")
        visit = super(DoctorVisit, self).create(vals)
        if vals.get('diagnosis_id'):
            self._create_diagnosis_record(visit)
        return visit

    def write(self, vals):
        if 'diagnosis_id' in vals:
            self._create_diagnosis_record(self)
        return super(DoctorVisit, self).write(vals)

    def unlink(self):
        if any(self.search([('diagnosis_id', '!=', False)])):
            raise ValidationError("You cannot delete or archive visits that have associated diagnoses.")
        return super(DoctorVisit, self).unlink()

    def action_confirm_visit(self):
        self.write({'appointment_confirmed': True})

    def _create_diagnosis_record(self, visit):
        self.env['hospital.diagnosis'].create({
            'doctor_id': visit.doctor_id.id,
            'patient_id': visit.patient_id.id,
            'disease_id': visit.diagnosis_id.id,
            'treatment': visit.recommendations,
            'diagnosis_date': fields.Date.today(),
            'doctor_visit_id': visit.id,
            'research_directory_ids': [(6, 0, visit.research_directory_ids.ids)],
        })