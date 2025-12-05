# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PatrimoineSupplier(models.Model):
    _name = 'patrimoine.supplier'
    _description = 'Fournisseur / Vendeur'
    _order = 'name'

    name = fields.Char(
        string='Nom',
        required=True,
        help="Nom du fournisseur ou vendeur"
    )

    code = fields.Char(
        string='Code',
        help="Code du fournisseur"
    )

    supplier_type = fields.Selection([
        ('manufacturer', 'Fabricant'),
        ('distributor', 'Distributeur'),
        ('retailer', 'Détaillant'),
        ('service', 'Prestataire de service'),
        ('other', 'Autre'),
    ], string='Type', default='distributor')

    # Contact information
    contact_person = fields.Char(
        string='Personne de contact'
    )

    phone = fields.Char(
        string='Téléphone'
    )

    mobile = fields.Char(
        string='Mobile'
    )

    email = fields.Char(
        string='Email'
    )

    website = fields.Char(
        string='Site Web'
    )

    # Address
    street = fields.Char(string='Rue')
    street2 = fields.Char(string='Rue 2')
    city = fields.Char(string='Ville')
    state_id = fields.Many2one(
        'res.country.state',
        string='État/Province'
    )
    zip = fields.Char(string='Code postal')
    country_id = fields.Many2one(
        'res.country',
        string='Pays'
    )

    # Financial info
    tax_id = fields.Char(
        string='Identifiant fiscal',
        help="Numéro d'identification fiscale"
    )

    payment_terms = fields.Text(
        string='Conditions de paiement'
    )

    # Products & Services
    products_services = fields.Text(
        string='Produits & Services',
        help="Description des produits et services proposés"
    )

    warranty_policy = fields.Text(
        string='Politique de garantie'
    )

    # Relationships
    equipment_ids = fields.One2many(
        'patrimoine.equipment',
        'supplier_id',
        string='Équipements fournis'
    )

    equipment_count = fields.Integer(
        string='Nombre d\'équipements',
        compute='_compute_equipment_count'
    )

    # Rating
    rating = fields.Selection([
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐'),
    ], string='Évaluation')

    notes = fields.Text(string='Notes')

    active = fields.Boolean(
        string='Actif',
        default=True
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)

    def action_view_equipment(self):
        """Voir les équipements fournis par ce fournisseur"""
        self.ensure_one()
        return {
            'name': _('Équipements - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.equipment',
            'view_mode': 'tree,kanban,form',
            'domain': [('supplier_id', '=', self.id)],
            'context': {'default_supplier_id': self.id}
        }
