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
        ('unique_appointment', 'UNIQUE(doctor_id, visit_date, visit_time)',
         'An appointment already exists for this doctor at this time.')
    ]

    @api.constrains('visit_date', 'visit_time')
    def _check_visit_time(self):
        for record in self:
            schedule = self.env['doctor.schedule'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('schedule_date', '=', record.visit_date),
                ('start_time', '<=', record.visit_time),
                ('end_time', '>', record.visit_time)
            ])
            if not schedule:
                raise ValidationError("The visit time does not fall within the doctor's available schedule.")
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
        if 'visit_time' in vals or 'doctor_id' in vals:
            self._check_visit_time()
        if 'diagnosis_id' in vals:
            self._create_diagnosis_record(self)
        return super(DoctorVisit, self).write(vals)

    def unlink(self):
        if any(visit.diagnosis_id for visit in self):
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

    def action_create_visit(self):
        self.ensure_one()
        vals = {
            'doctor_id': self.doctor_id.id,
            'patient_id': self.id,
            'visit_date': self.visit_date,
            'visit_time': self.visit_time,
        }
        return self.create(vals)

    def action_open_reschedule_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reschedule Visit',
            'res_model': 'reschedule.visit.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('hospital.view_reschedule_visit_wizard_form').id,
            'target': 'new',
            'context': {
                'default_visit_id': self.id,
                'default_doctor_id': self.doctor_id.id,
                'default_visit_date': self.visit_date,
                'default_visit_time': self.visit_time,
            }
        }