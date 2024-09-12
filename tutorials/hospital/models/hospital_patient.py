from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'person.base'
    _description = 'Information about patients'

    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    passport_number = fields.Char(string='Passport Number')
    contact_person_id = fields.Many2one('contact.person', string='Contact Person')
    personal_doctor_id = fields.Many2one('hospital.doctor', string='Personal Doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = fields.Date.from_string(record.birth_date)
                age = today.year - birth_date.year
                if (today.month, today.day) < (birth_date.month, birth_date.day):
                    age -= 1
                record.age = age

    @api.model
    def create(self, vals):
        record = super(HospitalPatient, self).create(vals)
        if vals.get('personal_doctor_id'):
            self._create_doctor_assignment_history(record)
        return record

    def write(self, vals):
        res = super(HospitalPatient, self).write(vals)
        if vals.get('personal_doctor_id'):
            self._create_doctor_assignment_history(self)
        return res

    def _create_doctor_assignment_history(self, patient):
        if patient.personal_doctor_id:
            existing_history = self.env['doctor.assignment.history'].search([
                ('patient_id', '=', patient.id),
                ('doctor_id', '=', patient.personal_doctor_id.id)
            ])
            if not existing_history:
                self.env['doctor.assignment.history'].create({
                    'patient_id': patient.id,
                    'doctor_id': patient.personal_doctor_id.id,
                    'assignment_date': fields.Date.today()
                })

    def action_mass_assign_doctor(self):
        return {
            'name': 'Mass Assign Doctor',
            'type': 'ir.actions.act_window',
            'res_model': 'mass.assign.doctor.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('hospital.view_mass_assign_doctor_wizard').id,
            'target': 'new',
        }

    def action_schedule_visit(self):
        self.ensure_one()
        if not self.personal_doctor_id:
            raise ValidationError("Personal doctor must be set before scheduling a visit.")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Schedule Visit',
            'view_mode': 'form',
            'view_id': self.env.ref('hospital.view_doctor_visit_form').id,
            'res_model': 'doctor.visit',
            'target': 'new',
            'context': {
                'default_doctor_id': self.personal_doctor_id.id,
                'default_patient_id': self.id
            }
        }