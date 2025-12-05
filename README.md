# Gestion du Patrimoine ENSAH

## Description

Module complet de gestion du patrimoine de l'École Nationale des Sciences Appliquées d'Al-Hoceima (ENSAH).

Ce module permet de :
- 📦 Gérer l'inventaire des équipements (ordinateurs, projecteurs, mobilier, matériel de laboratoire, etc.)
- 🔧 Suivre les interventions de maintenance et réparations
- 📍 Organiser les équipements par localisation (bâtiments, salles, labs)
- 👥 Assigner des responsables et techniciens
- 💰 Suivre les coûts d'acquisition et de maintenance
- 📊 Générer des rapports et statistiques
- 🏷️ Utiliser des codes-barres/QR codes pour l'identification

## Fonctionnalités Principales

### Gestion des Équipements
- Fiche complète pour chaque équipement
- Catégorisation (IT, Lab, Mobilier, Audiovisuel, etc.)
- Suivi de la localisation
- Gestion du cycle de vie (disponible, en utilisation, maintenance, retiré)
- Suivi de la garantie
- Historique complet des interventions

### Gestion des Interventions
- Demandes de maintenance et réparations
- Workflow complet : brouillon → soumis → assigné → en cours → terminé
- Affectation de techniciens
- Suivi des pièces utilisées
- Calcul automatique des coûts
- Maintenance préventive programmée
- Priorités (urgente, haute, normale, basse)

### Configuration
- Catégories d'équipements personnalisables
- Localisations (bâtiments, étages, salles)
- Gestion des fournisseurs
- Droits d'accès par groupes (utilisateur, technicien, manager)

### Rapports
- Fiche équipement détaillée (PDF)
- Bon d'intervention (PDF)
- Tableaux de bord et statistiques
- Vues pivot et graphiques

## Installation

1. Copier le module dans le dossier `addons` de votre instance Odoo
2. Mettre à jour la liste des modules
3. Installer le module "Gestion du Patrimoine ENSAH"

## Dépendances

- `base` : Module de base Odoo
- `mail` : Pour le chatter et suivi
- `web` : Interface web
- `contacts_management` : Module de gestion des contacts (pour techniciens et staff)

## Configuration Initiale

1. **Créer les localisations** : Configuration → Localisations
2. **Vérifier les catégories** : Configuration → Catégories (déjà pré-remplies)
3. **Ajouter les fournisseurs** : Configuration → Fournisseurs
4. **Configurer les utilisateurs** : Assigner les groupes (Utilisateur/Technicien/Manager)

## Utilisation

### Ajouter un Équipement
1. Aller dans Équipements → Tous les Équipements
2. Cliquer sur "Créer"
3. Remplir les informations (nom, catégorie, localisation, etc.)
4. Sauvegarder

### Créer une Intervention
1. Depuis la fiche équipement, cliquer sur "Créer Intervention"
2. OU : Aller dans Interventions → Toutes les Interventions → Créer
3. Remplir la description du problème
4. Soumettre la demande
5. Le technicien peut ensuite l'assigner, démarrer et terminer l'intervention

## Groupes de Sécurité

- **Utilisateur** : Peut voir les équipements, créer des demandes d'intervention
- **Technicien** : Peut modifier les équipements, gérer toutes les interventions
- **Manager** : Accès complet, peut supprimer, accès à la configuration

## Auteur

Développé par : Abdelkarim Oubakhayi
Institution : ENSAH (École Nationale des Sciences Appliquées d'Al-Hoceima)
Site web : https://www.ensah.ma

## Licence

LGPL-3

## Version

Version 17.0.1.0.0 pour Odoo 17.0
