# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta


class PatrimoineEquipment(models.Model):
    _name = 'patrimoine.equipment'
    _description = 'Équipement / Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'reference desc, name'

    # ==================== IDENTIFICATION ====================
    reference = fields.Char(
        string='Référence',
        required=True,
        readonly=True,
        default=lambda self: _('Nouveau'),
        copy=False,
        tracking=True
    )

    name = fields.Char(
        string='Nom de l\'équipement',
        required=True,
        tracking=True,
        help="Nom descriptif de l'équipement (ex: Ordinateur Dell Latitude 5420)"
    )

    barcode = fields.Char(
        string='Code-barres / QR Code',
        copy=False,
        tracking=True,
        help="Code-barres ou QR code pour identification rapide"
    )

    # ==================== CATÉGORIE & CLASSIFICATION ====================
    category_id = fields.Many2one(
        'patrimoine.equipment.category',
        string='Catégorie',
        required=True,
        tracking=True,
        ondelete='restrict',
        help="Type d'équipement (IT, Lab, Mobilier, etc.)"
    )

    sub_category = fields.Char(
        string='Sous-catégorie',
        tracking=True,
        help="Ex: Laptop, Desktop, Projecteur, etc."
    )

    # ==================== DESCRIPTION ====================
    description = fields.Text(
        string='Description',
        help="Description détaillée de l'équipement"
    )

    specifications = fields.Html(
        string='Spécifications techniques',
        help="Caractéristiques techniques détaillées"
    )

    serial_number = fields.Char(
        string='Numéro de série',
        copy=False,
        tracking=True
    )

    model = fields.Char(
        string='Modèle',
        tracking=True
    )

    brand = fields.Char(
        string='Marque',
        tracking=True,
        help="Fabricant ou marque de l'équipement"
    )

    # ==================== LOCALISATION ====================
    location_id = fields.Many2one(
        'patrimoine.location',
        string='Localisation',
        required=True,
        tracking=True,
        ondelete='restrict',
        help="Emplacement actuel de l'équipement"
    )

    building = fields.Char(
        related='location_id.building',
        string='Bâtiment',
        store=True,
        readonly=True
    )

    floor = fields.Char(
        related='location_id.floor',
        string='Étage',
        store=True,
        readonly=True
    )

    # ==================== RESPONSABILITÉ ====================
    responsible_id = fields.Many2one(
        'res.partner',
        string='Responsable',
        tracking=True,
        help="Personne responsable de cet équipement"
    )

    assigned_to_id = fields.Many2one(
        'res.partner',
        string='Assigné à',
        tracking=True,
        help="Utilisateur actuel de l'équipement"
    )

    # ==================== ACQUISITION ====================
    supplier_id = fields.Many2one(
        'patrimoine.supplier',
        string='Fournisseur',
        tracking=True,
        ondelete='restrict',
        help="Fournisseur ou vendeur"
    )

    purchase_date = fields.Date(
        string='Date d\'achat',
        tracking=True,
        default=fields.Date.today
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True
    )

    purchase_price = fields.Monetary(
        string='Prix d\'achat',
        currency_field='currency_id',
        tracking=True
    )

    invoice_reference = fields.Char(
        string='Référence facture',
        tracking=True
    )

    # ==================== GARANTIE ====================
    warranty_start_date = fields.Date(
        string='Début garantie',
        tracking=True
    )

    warranty_duration = fields.Integer(
        string='Durée garantie (mois)',
        default=12,
        tracking=True
    )

    warranty_end_date = fields.Date(
        string='Fin garantie',
        compute='_compute_warranty_end_date',
        store=True
    )

    is_under_warranty = fields.Boolean(
        string='Sous garantie',
        compute='_compute_is_under_warranty',
        search='_search_is_under_warranty'
    )

    # ==================== ÉTAT & LIFECYCLE ====================
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('available', 'Disponible'),
        ('in_use', 'En utilisation'),
        ('maintenance', 'En maintenance'),
        ('repair', 'En réparation'),
        ('retired', 'Retiré'),
        ('lost', 'Perdu/Volé'),
    ], string='État', default='draft', required=True, tracking=True)

    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Bon'),
        ('fair', 'Moyen'),
        ('poor', 'Mauvais'),
        ('broken', 'En panne'),
    ], string='Condition', default='good', tracking=True)

    activation_date = fields.Date(
        string='Date de mise en service',
        tracking=True
    )

    retirement_date = fields.Date(
        string='Date de retrait',
        tracking=True
    )

    retirement_reason = fields.Text(
        string='Raison du retrait'
    )

    # ==================== INTERVENTIONS ====================
    intervention_ids = fields.One2many(
        'patrimoine.intervention',
        'equipment_id',
        string='Interventions'
    )

    intervention_count = fields.Integer(
        string='Nombre d\'interventions',
        compute='_compute_intervention_count'
    )

    last_intervention_date = fields.Date(
        string='Dernière intervention',
        compute='_compute_last_intervention_date',
        store=True
    )

    total_intervention_cost = fields.Monetary(
        string='Coût total interventions',
        compute='_compute_total_intervention_cost',
        currency_field='currency_id'
    )

    # ==================== MAINTENANCE PRÉVENTIVE ====================
    requires_preventive_maintenance = fields.Boolean(
        string='Maintenance préventive requise',
        default=False
    )

    maintenance_frequency = fields.Integer(
        string='Fréquence maintenance (jours)',
        default=90,
        help="Nombre de jours entre chaque maintenance préventive"
    )

    next_maintenance_date = fields.Date(
        string='Prochaine maintenance',
        compute='_compute_next_maintenance_date',
        store=True
    )

    # ==================== DIVERS ====================
    notes = fields.Html(string='Notes')

    active = fields.Boolean(
        string='Actif',
        default=True,
        help="Décocher pour archiver l'équipement"
    )

    image = fields.Image(
        string='Photo',
        max_width=1024,
        max_height=1024
    )

    # ==================== COMPUTED FIELDS ====================
    @api.depends('warranty_start_date', 'warranty_duration')
    def _compute_warranty_end_date(self):
        for record in self:
            if record.warranty_start_date and record.warranty_duration:
                record.warranty_end_date = record.warranty_start_date + timedelta(
                    days=record.warranty_duration * 30
                )
            else:
                record.warranty_end_date = False

    @api.depends('warranty_end_date')
    def _compute_is_under_warranty(self):
        today = fields.Date.today()
        for record in self:
            record.is_under_warranty = (
                record.warranty_end_date and record.warranty_end_date >= today
            )

    def _search_is_under_warranty(self, operator, value):
        today = fields.Date.today()
        if operator == '=' and value:
            return [('warranty_end_date', '>=', today)]
        elif operator == '=' and not value:
            return ['|', ('warranty_end_date', '<', today), ('warranty_end_date', '=', False)]
        return []

    @api.depends('intervention_ids')
    def _compute_intervention_count(self):
        for record in self:
            record.intervention_count = len(record.intervention_ids)

    @api.depends('intervention_ids.intervention_date')
    def _compute_last_intervention_date(self):
        for record in self:
            if record.intervention_ids:
                record.last_intervention_date = max(
                    record.intervention_ids.mapped('intervention_date')
                )
            else:
                record.last_intervention_date = False

    @api.depends('intervention_ids.total_cost')
    def _compute_total_intervention_cost(self):
        for record in self:
            record.total_intervention_cost = sum(
                record.intervention_ids.mapped('total_cost')
            )

    @api.depends('last_intervention_date', 'maintenance_frequency', 'requires_preventive_maintenance')
    def _compute_next_maintenance_date(self):
        for record in self:
            if record.requires_preventive_maintenance and record.maintenance_frequency:
                if record.last_intervention_date:
                    record.next_maintenance_date = record.last_intervention_date + timedelta(
                        days=record.maintenance_frequency
                    )
                elif record.activation_date:
                    record.next_maintenance_date = record.activation_date + timedelta(
                        days=record.maintenance_frequency
                    )
                else:
                    record.next_maintenance_date = fields.Date.today() + timedelta(
                        days=record.maintenance_frequency
                    )
            else:
                record.next_maintenance_date = False

    # ==================== CONSTRAINTS ====================
    @api.constrains('barcode')
    def _check_unique_barcode(self):
        for record in self:
            if record.barcode:
                duplicate = self.search([
                    ('barcode', '=', record.barcode),
                    ('id', '!=', record.id)
                ])
                if duplicate:
                    raise ValidationError(
                        _("Le code-barres '%s' est déjà utilisé par l'équipement '%s'") %
                        (record.barcode, duplicate.name)
                    )

    @api.constrains('purchase_price')
    def _check_purchase_price(self):
        for record in self:
            if record.purchase_price < 0:
                raise ValidationError(_("Le prix d'achat ne peut pas être négatif"))

    # ==================== CRUD & SEQUENCES ====================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'patrimoine.equipment.sequence'
                ) or _('Nouveau')
        return super(PatrimoineEquipment, self).create(vals_list)

    # ==================== ACTIONS ====================
    def action_set_available(self):
        self.write({'state': 'available'})

    def action_set_in_use(self):
        self.write({'state': 'in_use'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})

    def action_set_retired(self):
        self.write({
            'state': 'retired',
            'retirement_date': fields.Date.today()
        })

    def action_view_interventions(self):
        """Ouvrir la liste des interventions pour cet équipement"""
        self.ensure_one()
        return {
            'name': _('Interventions - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.intervention',
            'view_mode': 'tree,form,kanban',
            'domain': [('equipment_id', '=', self.id)],
            'context': {'default_equipment_id': self.id}
        }

    def action_create_intervention(self):
        """Créer une nouvelle intervention pour cet équipement"""
        self.ensure_one()
        return {
            'name': _('Nouvelle Intervention'),
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.intervention',
            'view_mode': 'form',
            'context': {
                'default_equipment_id': self.id,
                'default_location_id': self.location_id.id,
            },
            'target': 'new',
        }
