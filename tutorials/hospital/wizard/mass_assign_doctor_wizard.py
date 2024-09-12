from odoo import models, fields, api


class MassAssignDoctorWizard(models.TransientModel):
    _name = 'mass.assign.doctor.wizard'
    _description = 'Mass Assign Doctor Wizard'

    new_doctor_id = fields.Many2one('hospital.doctor', string='New Doctor', required=True)

    def assign_doctor(self):
        active_ids = self.env.context.get('active_ids', [])
        patients = self.env['hospital.patient'].browse(active_ids)

        for patient in patients:
            old_doctor = patient.personal_doctor_id
            if patient.personal_doctor_id != self.new_doctor_id:
                patient.write({'personal_doctor_id': self.new_doctor_id})

                if old_doctor:
                    existing_history = self.env['doctor.assignment.history'].search([
                        ('patient_id', '=', patient.id),
                        ('doctor_id', '=', self.new_doctor_id.id)
                    ])
                    if not existing_history:
                        self.env['doctor.assignment.history'].create({
                            'patient_id': patient.id,
                            'doctor_id': self.new_doctor_id.id,
                            'assignment_date': fields.Date.today()
                        })

        return {'type': 'ir.actions.act_window_close'}