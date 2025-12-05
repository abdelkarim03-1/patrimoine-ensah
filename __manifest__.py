# -*- coding: utf-8 -*-
{
    'name': "Gestion du Patrimoine ENSAH",
    'summary': "Système de gestion des équipements, inventaires et interventions",
    'description': """
        Module complet de gestion du patrimoine de l'ENSAH
        ===================================================

        Fonctionnalités principales:
        * Gestion des équipements (ordinateurs, projecteurs, mobilier, etc.)
        * Suivi des inventaires par localisation
        * Gestion des interventions et maintenances
        * Suivi des réparations et coûts
        * Affectation des techniciens
        * Rapports et tableaux de bord
        * Code-barres et QR codes
        * Alertes et notifications
    """,
    'author': "abdelkarim oubakhayi",
    'website': "https://www.ensah.ma",
    'category': 'Operations/Inventory',
    'version': '17.0.1.0.0',

    # Dependencies
    'depends': [
        'base',
        'mail',
        'web',
    ],

    # Data files
    'data': [
        # Security
        'security/patrimoine_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sequence_data.xml',
        'data/equipment_category_data.xml',
        'data/intervention_type_data.xml',

        # Views (load actions first, then menus that reference them)
        'views/equipment_views.xml',
        'views/intervention_views.xml',
        'views/category_views.xml',
        'views/location_views.xml',
        'views/supplier_views.xml',
        'views/dashboard_views.xml',
        'views/patrimoine_menus.xml',  # MUST be last - references actions above

        # Reports
        'reports/equipment_report_templates.xml',
        'reports/intervention_report_templates.xml',
    ],

    # Demo data (optional)
    'demo': [
        'demo/demo_data.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
