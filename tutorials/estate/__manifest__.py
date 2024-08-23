{
    'name': 'Not Real Estate',
    'version': '1.0.0',
    'category': 'Sales/CRM',
    'sequence': 5,
    'summary': 'Testing creation',
    'description': "",
    'website': 'https://www.odoo.com/',
    'depends': [
        'base_setup'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}