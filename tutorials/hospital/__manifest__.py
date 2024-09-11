{
    'name': 'Hospital',
    'version': '1.0.0',
    'category': 'Hidden',
    'sequence': 5,
    'summary': 'Hospital module',
    'description': "",
    'website': 'https://www.odoo.com/',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctor_visit_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_doctor_views.xml',
        'views/disease_type_views.xml',
        'views/disease_directory_views.xml',
        'views/diagnosis_views.xml',
        'views/contact_person_views.xml',
        'views/doctor_assignment_history_views.xml',
        'views/specialty_type_views.xml',
        'views/research_directory_views.xml',
        'views/research_type_views.xml',
        'views/sample_type_views.xml',
        'views/doctor_schedule_views.xml',
        'views/hospital_menu.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}