# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PatrimoineIntervention(models.Model):
    _name = 'patrimoine.intervention'
    _description = 'Intervention / Maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'intervention_date desc, id desc'

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
        string='Titre',
        required=True,
        tracking=True,
        help="Titre court de l'intervention"
    )

    # ==================== ÉQUIPEMENT CONCERNÉ ====================
    equipment_id = fields.Many2one(
        'patrimoine.equipment',
        string='Équipement',
        required=True,
        tracking=True,
        ondelete='restrict',
        help="Équipement concerné par l'intervention"
    )

    equipment_reference = fields.Char(
        related='equipment_id.reference',
        string='Réf. Équipement',
        store=True,
        readonly=True
    )

    equipment_category_id = fields.Many2one(
        related='equipment_id.category_id',
        string='Catégorie Équipement',
        store=True,
        readonly=True
    )

    # ==================== TYPE D'INTERVENTION ====================
    intervention_type = fields.Selection([
        ('maintenance', 'Maintenance Préventive'),
        ('repair', 'Réparation'),
        ('inspection', 'Inspection'),
        ('installation', 'Installation'),
        ('upgrade', 'Mise à niveau'),
        ('cleaning', 'Nettoyage'),
        ('other', 'Autre'),
    ], string='Type', required=True, default='repair', tracking=True)

    priority = fields.Selection([
        ('low', 'Basse'),
        ('normal', 'Normale'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ], string='Priorité', default='normal', required=True, tracking=True)

    # ==================== DATES ====================
    request_date = fields.Datetime(
        string='Date de demande',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )

    intervention_date = fields.Date(
        string='Date d\'intervention',
        tracking=True,
        help="Date prévue ou réalisée de l'intervention"
    )

    start_datetime = fields.Datetime(
        string='Début',
        tracking=True
    )

    end_datetime = fields.Datetime(
        string='Fin',
        tracking=True
    )

    duration = fields.Float(
        string='Durée (heures)',
        compute='_compute_duration',
        store=True,
        help="Durée en heures"
    )

    # ==================== DEMANDEUR ====================
    requester_id = fields.Many2one(
        'res.partner',
        string='Demandeur',
        tracking=True,
        help="Personne ayant demandé l'intervention"
    )

    requester_phone = fields.Char(
        related='requester_id.phone',
        string='Tél. Demandeur',
        readonly=True
    )

    requester_email = fields.Char(
        related='requester_id.email',
        string='Email Demandeur',
        readonly=True
    )

    # ==================== TECHNICIEN ====================
    technician_id = fields.Many2one(
        'res.partner',
        string='Technicien',
        tracking=True,
        help="Technicien assigné à l'intervention"
    )

    technician_phone = fields.Char(
        related='technician_id.phone',
        string='Tél. Technicien',
        readonly=True
    )

    # ==================== LOCALISATION ====================
    location_id = fields.Many2one(
        'patrimoine.location',
        string='Localisation',
        tracking=True,
        help="Lieu de l'intervention"
    )

    building = fields.Char(
        related='location_id.building',
        string='Bâtiment',
        readonly=True
    )

    # ==================== DESCRIPTION ====================
    description = fields.Html(
        string='Description du problème',
        required=True,
        help="Description détaillée du problème ou de la demande"
    )

    diagnostic = fields.Html(
        string='Diagnostic',
        help="Diagnostic du technicien"
    )

    work_done = fields.Html(
        string='Travail effectué',
        help="Description du travail réalisé"
    )

    recommendations = fields.Html(
        string='Recommandations',
        help="Recommandations pour éviter de futurs problèmes"
    )

    # ==================== ÉTAT ====================
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumise'),
        ('assigned', 'Assignée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft', required=True, tracking=True)

    # ==================== PIÈCES & COÛTS ====================
    spare_parts_ids = fields.One2many(
        'patrimoine.intervention.spare.part',
        'intervention_id',
        string='Pièces utilisées'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True
    )

    labor_cost = fields.Monetary(
        string='Coût main d\'œuvre',
        currency_field='currency_id',
        tracking=True
    )

    spare_parts_cost = fields.Monetary(
        string='Coût pièces',
        compute='_compute_spare_parts_cost',
        store=True,
        currency_field='currency_id'
    )

    other_costs = fields.Monetary(
        string='Autres coûts',
        currency_field='currency_id',
        tracking=True
    )

    total_cost = fields.Monetary(
        string='Coût total',
        compute='_compute_total_cost',
        store=True,
        currency_field='currency_id'
    )

    # ==================== RÉSULTAT ====================
    resolution_status = fields.Selection([
        ('fixed', 'Réparé'),
        ('partially_fixed', 'Partiellement réparé'),
        ('not_fixed', 'Non réparé'),
        ('replaced', 'Remplacé'),
        ('needs_more_work', 'Nécessite plus de travail'),
    ], string='Statut de résolution', tracking=True)

    customer_satisfaction = fields.Selection([
        ('very_satisfied', 'Très satisfait'),
        ('satisfied', 'Satisfait'),
        ('neutral', 'Neutre'),
        ('dissatisfied', 'Insatisfait'),
        ('very_dissatisfied', 'Très insatisfait'),
    ], string='Satisfaction', tracking=True)

    # ==================== DIVERS ====================
    notes = fields.Html(string='Notes')

    attachments_count = fields.Integer(
        compute='_compute_attachments_count',
        string='Nombre de pièces jointes'
    )

    # ==================== COMPUTED FIELDS ====================
    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration = delta.total_seconds() / 3600  # Convert to hours
            else:
                record.duration = 0.0

    @api.depends('spare_parts_ids.subtotal')
    def _compute_spare_parts_cost(self):
        for record in self:
            record.spare_parts_cost = sum(record.spare_parts_ids.mapped('subtotal'))

    @api.depends('labor_cost', 'spare_parts_cost', 'other_costs')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = (
                record.labor_cost +
                record.spare_parts_cost +
                record.other_costs
            )

    def _compute_attachments_count(self):
        for record in self:
            record.attachments_count = self.env['ir.attachment'].search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', record.id)
            ])

    # ==================== CONSTRAINTS ====================
    @api.constrains('start_datetime', 'end_datetime')
    def _check_datetime_logic(self):
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.end_datetime < record.start_datetime:
                    raise ValidationError(
                        _("La date de fin doit être postérieure à la date de début")
                    )

    @api.constrains('labor_cost', 'other_costs')
    def _check_costs(self):
        for record in self:
            if record.labor_cost < 0 or record.other_costs < 0:
                raise ValidationError(_("Les coûts ne peuvent pas être négatifs"))

    # ==================== CRUD & SEQUENCES ====================
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', _('Nouveau')) == _('Nouveau'):
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'patrimoine.intervention.sequence'
                ) or _('Nouveau')
        return super(PatrimoineIntervention, self).create(vals_list)

    # ==================== ONCHANGE ====================
    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.location_id = self.equipment_id.location_id

    # ==================== WORKFLOW ACTIONS ====================
    def action_submit(self):
        """Soumettre l'intervention"""
        self.write({
            'state': 'submitted',
            'request_date': fields.Datetime.now()
        })

    def action_assign(self):
        """Assigner à un technicien"""
        if not self.technician_id:
            raise UserError(_("Veuillez assigner un technicien avant de valider"))
        self.write({'state': 'assigned'})

    def action_start(self):
        """Démarrer l'intervention"""
        self.write({
            'state': 'in_progress',
            'start_datetime': fields.Datetime.now()
        })
        # Mettre l'équipement en maintenance
        if self.equipment_id.state == 'in_use':
            self.equipment_id.write({'state': 'maintenance'})

    def action_complete(self):
        """Terminer l'intervention"""
        if not self.work_done:
            raise UserError(_("Veuillez décrire le travail effectué avant de terminer"))

        self.write({
            'state': 'done',
            'end_datetime': fields.Datetime.now(),
            'intervention_date': fields.Date.today()
        })

        # Remettre l'équipement disponible ou en utilisation
        if self.equipment_id.state == 'maintenance':
            if self.resolution_status == 'fixed':
                self.equipment_id.write({'state': 'available'})
            elif self.resolution_status == 'not_fixed':
                self.equipment_id.write({'state': 'repair'})

    def action_cancel(self):
        """Annuler l'intervention"""
        self.write({'state': 'cancelled'})

    def action_reset_to_draft(self):
        """Remettre en brouillon"""
        self.write({'state': 'draft'})

    # ==================== SMART BUTTONS ====================
    def action_view_equipment(self):
        """Voir l'équipement"""
        self.ensure_one()
        return {
            'name': self.equipment_id.name,
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.equipment',
            'res_id': self.equipment_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_attachments(self):
        """Voir les pièces jointes"""
        self.ensure_one()
        return {
            'name': _('Pièces jointes - %s') % self.reference,
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'kanban,tree,form',
            'domain': [('res_model', '=', self._name), ('res_id', '=', self.id)],
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
            }
        }


class PatrimoineInterventionSparePart(models.Model):
    """Pièces de rechange utilisées dans une intervention"""
    _name = 'patrimoine.intervention.spare.part'
    _description = 'Pièce utilisée dans intervention'

    intervention_id = fields.Many2one(
        'patrimoine.intervention',
        string='Intervention',
        required=True,
        ondelete='cascade'
    )

    name = fields.Char(
        string='Pièce',
        required=True,
        help="Nom de la pièce de rechange"
    )

    reference = fields.Char(
        string='Référence',
        help="Référence fabricant"
    )

    quantity = fields.Float(
        string='Quantité',
        default=1.0,
        required=True
    )

    currency_id = fields.Many2one(
        related='intervention_id.currency_id',
        string='Devise',
        readonly=True
    )

    unit_price = fields.Monetary(
        string='Prix unitaire',
        currency_field='currency_id',
        required=True
    )

    subtotal = fields.Monetary(
        string='Sous-total',
        compute='_compute_subtotal',
        store=True,
        currency_field='currency_id'
    )

    notes = fields.Text(string='Notes')

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price

    @api.constrains('quantity', 'unit_price')
    def _check_values(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_("La quantité doit être positive"))
            if record.unit_price < 0:
                raise ValidationError(_("Le prix unitaire ne peut pas être négatif"))
