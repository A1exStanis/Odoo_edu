from odoo import fields, models, api, Command


class InheritedProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super(InheritedProperty, self).action_sold()
        for record in self:
            if record.buyer_id:
                selling_price = record.selling_price
                service_charge = selling_price * 0.06
                self.env['account.move'].create({
                    'partner_id': record.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_date': fields.Date.context_today(self),
                    'invoice_line_ids': [
                        Command.create({
                            'name': 'Property Sale',
                            'quantity': 1,
                            'price_unit': selling_price
                        }),
                        Command.create({
                            'name': 'Administrative Fees',
                            'quantity': 1,
                            'price_unit': 100
                        }),
                        Command.create({
                            'name': 'Service Charge (6%)',
                            'quantity': 1,
                            'price_unit': service_charge
                        })
                    ]

                })

        return res
