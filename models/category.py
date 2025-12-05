# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PatrimoineEquipmentCategory(models.Model):
    _name = 'patrimoine.equipment.category'
    _description = 'Catégorie d\'équipement'
    _order = 'name'

    name = fields.Char(
        string='Nom',
        required=True,
        translate=True,
        help="Nom de la catégorie (ex: Informatique, Mobilier, Laboratoire)"
    )

    code = fields.Char(
        string='Code',
        required=True,
        help="Code court pour identification (ex: IT, LAB, MOBI)"
    )

    description = fields.Text(
        string='Description',
        translate=True
    )

    parent_id = fields.Many2one(
        'patrimoine.equipment.category',
        string='Catégorie parente',
        ondelete='restrict',
        help="Catégorie parente pour créer une hiérarchie"
    )

    child_ids = fields.One2many(
        'patrimoine.equipment.category',
        'parent_id',
        string='Sous-catégories'
    )

    equipment_ids = fields.One2many(
        'patrimoine.equipment',
        'category_id',
        string='Équipements'
    )

    equipment_count = fields.Integer(
        string='Nombre d\'équipements',
        compute='_compute_equipment_count'
    )

    color = fields.Integer(
        string='Couleur',
        help="Couleur pour l'affichage dans l'interface"
    )

    active = fields.Boolean(
        string='Actif',
        default=True
    )

    @api.depends('equipment_ids')
    def _compute_equipment_count(self):
        for record in self:
            record.equipment_count = len(record.equipment_ids)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code de catégorie doit être unique!')
    ]

    def name_get(self):
        """Afficher le nom avec le code"""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result

    def action_view_equipment(self):
        """Voir les équipements de cette catégorie"""
        self.ensure_one()
        return {
            'name': _('Équipements - %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'patrimoine.equipment',
            'view_mode': 'tree,kanban,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id}
        }
