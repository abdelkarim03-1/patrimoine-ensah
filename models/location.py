# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PatrimoineLocation(models.Model):
    _name = 'patrimoine.location'
    _description = 'Localisation / Emplacement'
    _order = 'building, floor, name'

    name = fields.Char(
        string='Nom',
        required=True,
        help="Nom de la salle ou zone (ex: Salle 101, Bureau Doyen, Lab Chimie)"
    )

    code = fields.Char(
        string='Code',
        help="Code court pour identification (ex: S101, BD, LC)"
    )

    building = fields.Char(
        string='Bâtiment',
        required=True,
        help="Nom ou numéro du bâtiment"
    )

    floor = fields.Char(
        string='Étage',
        help="Étage ou niveau (ex: RDC, 1er, 2ème)"
    )

    location_type = fields.Selection([
        ('office', 'Bureau'),
        ('classroom', 'Salle de classe'),
        ('lab', 'Laboratoire'),
        ('amphitheater', 'Amphithéâtre'),
        ('workshop', 'Atelier'),
        ('storage', 'Stockage'),
        ('common', 'Espace commun'),
        ('other', 'Autre'),
    ], string='Type', default='office')

    description = fields.Text(
        string='Description'
    )

    capacity = fields.Integer(
        string='Capacité',
        help="Nombre de personnes ou capacité de la salle"
    )

    surface_area = fields.Float(
        string='Surface (m²)',
        help="Surface en mètres carrés"
    )

    responsible_id = fields.Many2one(
        'res.partner',
        string='Responsable',
        help="Personne responsable de cet emplacement"
    )

    equipment_ids = fields.One2many(
        'patrimoine.equipment',
        'location_id',
        string='Équipements'
    )

    equipment_count = fields.Integer(
        string='Nombre d\'équipements',
        compute='_compute_equipment_count'
    )

    active = fields.Boolean(
        string='Actif',
        default=True
    )

    notes = fields.Text(string='Notes')

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code de localisation doit être unique!')
    ]

    def name_get(self):
        """Afficher un nom complet avec bâtiment et étage"""
        result = []
        for record in self:
            parts = []
            if record.building:
                parts.append(record.building)
            if record.floor:
                parts.append(record.floor)
            parts.append(record.name)
            name = ' - '.join(parts)
            result.append((record.id, name))
        return result

    def action_view_equipment(self):
        """Voir les équipements de cette localisation"""
        self.ensure_one()
        return {
            'name': _('Équipements - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.equipment',
            'view_mode': 'tree,kanban,form',
            'domain': [('location_id', '=', self.id)],
            'context': {'default_location_id': self.id}
        }
