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