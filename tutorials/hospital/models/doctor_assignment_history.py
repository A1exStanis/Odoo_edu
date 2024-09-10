from odoo import models, fields, api


class DoctorAssignmentHistory(models.Model):
    _name = 'doctor.assignment.history'
    _description = 'Doctor Assignment History'

    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    assignment_date = fields.Date(string='Assignment Date', required=True)

    @api.model
    def create(self, vals):
        if 'patient_id' not in vals or not vals['patient_id']:
            raise ValueError('patient_id is missing in values.')
        if 'doctor_id' not in vals or not vals['doctor_id']:
            raise ValueError('doctor_id is missing in values.')
        return super(DoctorAssignmentHistory, self).create(vals)