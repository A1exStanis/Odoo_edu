from odoo import models, fields


class ContactPerson(models.Model):
    _name = 'contact.person'
    _inherit = 'person.base'
    _description = 'Contact Person'

    relationship = fields.Char(string='Relationship')