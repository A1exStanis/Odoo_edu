from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'person.base'
    _description = 'Information about doctor'

    specialty = fields.Many2one('specialty.type', string='Specialty')
    is_intern = fields.Boolean(string='Intern', default=False)
    mentor_id = fields.Many2one('hospital.doctor',
                                string='Mentor', domain="[('id', '!=', id)]")
    schedule_ids = fields.One2many('doctor.schedule', 'doctor_id', string='Schedules')
    visit_ids = fields.One2many('doctor.visit', 'doctor_id', string='Visits')
    diagnosis_ids = fields.One2many('hospital.diagnosis', 'doctor_id', string='Diagnosis')
    doctor_history_ids = fields.One2many('doctor.assignment.history', 'doctor_id', string='Doctor Assignment History')

    @api.constrains('mentor_id')
    def _check_mentor(self):
        for record in self:
            if record.is_intern and record.mentor_id and record.mentor_id.is_intern:
                raise ValidationError('An intern cannot be selected as a mentor.')

    @api.model
    def create(self, vals):
        record = super(HospitalDoctor, self).create(vals)
        if record.is_intern and not record.mentor_id:
            raise ValidationError('Interns must have a mentor assigned.')
        return record

    def action_open_schedule_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Set Doctor Schedule',
            'view_mode': 'form',
            'res_model': 'doctor.schedule.wizard',
            'view_id': self.env.ref('hospital.view_doctor_schedule_wizard_form').id,
            'target': 'new',
            'context': {'default_doctor_id': self.id},
        }