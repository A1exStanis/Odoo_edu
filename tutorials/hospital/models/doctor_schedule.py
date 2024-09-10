from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DoctorSchedule(models.Model):
    _name = 'doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Date(string='Date', required=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)

    _sql_constraints = [
        ('unique_schedule', 'unique(doctor_id, date, start_time, end_time)',
         'The schedule entry must be unique for the doctor on the given date and time.')
    ]

    @api.constrains('start_time', 'end_time')
    def _check_schedule_times(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("The start time must be before the end time.")

            overlapping_schedules = self.search([
                ('doctor_id', '=', record.doctor_id.id),
                ('date', '=', record.date),
                ('id', '!=', record.id),
                '|', ('start_time', '<', record.end_time), ('end_time', '>', record.start_time)
            ])
            if overlapping_schedules:
                raise ValidationError("The specified time slot overlaps with another schedule.")