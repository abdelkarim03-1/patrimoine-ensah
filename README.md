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

### Pour les Collaborateurs (Clone depuis GitHub)

```bash
# 1. Cloner le repository
git clone https://github.com/abdelkarim03-1/patrimoine-ensah.git

# 2. Copier le module dans votre dossier addons Odoo
cp -r patrimoine-ensah /path/to/your/odoo/addons/patrimoine_ensah

# 3. Redémarrer Odoo
# Si vous utilisez Docker:
docker restart odoo-web-1

# Si vous utilisez Odoo en ligne de commande:
# Arrêter et redémarrer votre service Odoo
```

### Dans Odoo

1. Aller dans **Apps** (Applications)
2. Cliquer sur "Update Apps List" (Mettre à jour la liste des applications)
3. Rechercher "Gestion du Patrimoine ENSAH"
4. Cliquer sur **Install**
5. **Important:** Cocher "Load Demonstration Data" pour charger les données de test

### Données de Démonstration

Le module inclut des données de démonstration :
- 5 équipements (PC, projecteur, switch réseau, bureau)
- 4 interventions à différents états
- 3 fournisseurs
- Localisations de l'ENSAH
- Contacts (techniciens et responsables)

## Dépendances

- `base` : Module de base Odoo
- `mail` : Pour le chatter et suivi
- `web` : Interface web

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

Version 16.0.1.0.0 pour Odoo 16.0

## Contribution

Pour contribuer au projet :

1. Fork le repository
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -m 'Ajout de nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## Support

Pour toute question ou problème :
- GitHub Issues : https://github.com/abdelkarim03-1/patrimoine-ensah/issues
