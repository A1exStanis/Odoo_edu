from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    even_week_start_time = fields.Datetime(string='Even Week Start Time', required=True)
    even_week_end_time = fields.Datetime(string='Even Week End Time', required=True)

    odd_week_start_time = fields.Datetime(string='Odd Week Start Time', required=True)
    odd_week_end_time = fields.Datetime(string='Odd Week End Time', required=True)

    def _is_even_week(self, date):
        return date.isocalendar()[1] % 2 == 0

    def _is_odd_week(self, date):
        return date.isocalendar()[1] % 2 != 0

    def _create_schedule_for_week(self, doctor_id, start_date, end_date, start_time, end_time, is_even_week):
        current_date = start_date
        while current_date <= end_date:
            if (self._is_even_week(current_date) and is_even_week) or \
                    (self._is_odd_week(current_date) and not is_even_week):
                self.env['doctor.schedule'].create({
                    'doctor_id': doctor_id,
                    'schedule_date': current_date,
                    'start_time': datetime.combine(current_date, start_time),
                    'end_time': datetime.combine(current_date, end_time),
                })
            current_date += timedelta(days=1)

    def action_save_schedule(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise ValidationError("The start date cannot be later than the end date.")
        self._create_schedule_for_week(
            self.doctor_id.id,
            self.start_date,
            self.end_date,
            self.even_week_start_time.time(),
            self.even_week_end_time.time(),
            is_even_week=True
        )
        self._create_schedule_for_week(
            self.doctor_id.id,
            self.start_date,
            self.end_date,
            self.odd_week_start_time.time(),
            self.odd_week_end_time.time(),
            is_even_week=False
        )
