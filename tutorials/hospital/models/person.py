from odoo import models, fields, api


class Person(models.AbstractModel):
    _name = 'person.base'
    _description = 'Base Person Model'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    photo = fields.Binary(string='Photo')
    gender = fields.Selection(string='Gender',
                              selection=[('male', 'Male'), ('female', 'Female')])