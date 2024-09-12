from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RescheduleVisitWizard(models.TransientModel):
    _name = 'reschedule.visit.wizard'
    _description = 'Wizard to Reschedule a Visit'

    visit_id = fields.Many2one('doctor.visit', string='Visit', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    visit_date = fields.Date(string='Visit Date')
    visit_time = fields.Datetime(string='Visit Time')

    @api.onchange('doctor_id')
    def _onchange_doctor(self):
        if self.doctor_id:
            self.visit_date = False
            self.visit_time = False

    @api.onchange('visit_date')
    def _onchange_date(self):
        if self.visit_date:
            self.visit_time = False

    def action_reschedule(self):
        if not self.visit_date or not self.visit_time:
            raise ValidationError("Visit date and time must be specified.")

        # Check if the new appointment time is available
        if self.doctor_id:
            overlapping_visits = self.env['doctor.visit'].search([
                ('doctor_id', '=', self.doctor_id.id),
                ('visit_date', '=', self.visit_date),
                ('visit_time', '=', self.visit_time),
                ('id', '!=', self.visit_id.id)
            ])
            if overlapping_visits:
                raise ValidationError("The new appointment time conflicts with another appointment.")

        self.visit_id.write({
            'doctor_id': self.doctor_id.id or self.visit_id.doctor_id.id,
            'visit_date': self.visit_date or self.visit_id.visit_date,
            'visit_time': self.visit_time or self.visit_id.visit_time,
        })

        return {'type': 'ir.actions.act_window_close'}