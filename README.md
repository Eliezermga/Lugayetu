
# Préservation de la Langue Rund

Une application web Flask dédiée à la sauvegarde numérique de la langue Rund, une langue rare et précieuse qui fait partie du patrimoine culturel de l'humanité.

## 📋 Table des matières

- [À propos du projet](#à-propos-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Interface administrateur](#interface-administrateur)
- [Structure du projet](#structure-du-projet)
- [Technologies utilisées](#technologies-utilisées)
- [Contribution](#contribution)
- [Sécurité et confidentialité](#sécurité-et-confidentialité)

## 🎯 À propos du projet

Cette application web permet de collecter et préserver des enregistrements vocaux de la langue Rund. Les utilisateurs peuvent s'inscrire, lire des phrases en langue Rund et enregistrer leur prononciation pour créer une archive audio numérique accessible aux générations futures et aux chercheurs en linguistique.

### Objectifs du projet

- **Préservation culturelle** : Sauvegarder une langue en voie de disparition
- **Recherche linguistique** : Fournir des données pour la recherche académique
- **Accessibilité** : Créer une archive numérique facilement accessible
- **Participation communautaire** : Permettre à chacun de contribuer à la préservation

## ✨ Fonctionnalités

### Pour les utilisateurs
- **Inscription sécurisée** avec consentement explicite
- **Authentification** par email et mot de passe
- **Enregistrement audio** en temps réel dans le navigateur
- **Interface intuitive** pour lire et enregistrer des phrases
- **Prévisualisation** des enregistrements avant sauvegarde
- **Navigation responsive** adaptée aux appareils mobiles

### Pour les administrateurs
- **Tableau de bord** avec statistiques en temps réel
- **Gestion des utilisateurs** et de leurs enregistrements
- **Export des données** au format CSV
- **Lecture des enregistrements** directement dans l'interface
- **Suppression sélective** des données

## 🔧 Prérequis

- Python 3.11 ou supérieur
- PostgreSQL (base de données)
- Navigateur web moderne avec support audio
- Microphone pour les enregistrements

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone [URL_DU_REPO]
cd preservation-langue-rund
```

### 2. Installer les dépendances
```bash
pip install -r pyproject.toml
```

### 3. Configurer la base de données
Assurez-vous que PostgreSQL est installé et démarré, puis créez une base de données pour l'application.

## ⚙️ Configuration

### Variables d'environnement requises

Créez les variables d'environnement suivantes (dans Replit, utilisez l'outil Secrets) :

```bash
# OBLIGATOIRE - Clé secrète pour les sessions (générez une clé aléatoire forte)
SESSION_SECRET=votre_cle_secrete_forte_et_unique

# OBLIGATOIRE - URL de connexion à la base de données PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### Variables d'environnement optionnelles

```bash
# Création automatique d'un compte administrateur (optionnel)
CREATE_ADMIN_USER=true

# Email de l'administrateur (par défaut: admin@rund.local)
ADMIN_EMAIL=admin@votre-domaine.com

# Mot de passe administrateur (si non défini, un mot de passe aléatoire sera généré)
ADMIN_PASSWORD=votre_mot_de_passe_admin
```

## 🎮 Utilisation

### Démarrage de l'application

```bash
python main.py
```

L'application sera accessible sur `http://0.0.0.0:5000`

### Première utilisation

1. **Démarrez l'application** - Les tables de la base de données seront créées automatiquement
2. **Chargement des phrases** - Les phrases du fichier `phrases.txt` seront importées
3. **Création de l'admin** (si configuré) - Un compte administrateur sera créé

### Workflow utilisateur

1. **Accueil** - Visitez la page d'accueil pour comprendre le projet
2. **Inscription** - Créez un compte avec vos informations personnelles
3. **Consentement** - Acceptez la politique de confidentialité
4. **Connexion** - Connectez-vous avec vos identifiants
5. **Enregistrement** - Lisez et enregistrez les phrases proposées
6. **Contribution** - Répétez le processus pour enrichir l'archive

## 👨‍💼 Interface administrateur

### Accès administrateur

- URL : `http://0.0.0.0:5000/admin`
- Connectez-vous avec un compte administrateur

### Fonctionnalités disponibles

- **Statistiques** : Nombre total d'enregistrements, utilisateurs uniques, phrases enregistrées
- **Vue d'ensemble** : Liste détaillée de tous les enregistrements
- **Lecture audio** : Écoute directe des enregistrements
- **Export CSV** : Téléchargement de toutes les données
- **Gestion** : Suppression d'enregistrements ou d'utilisateurs

## 📁 Structure du projet

```
├── main.py                 # Application Flask principale
├── phrases.txt            # Phrases en langue Rund à enregistrer
├── static/
│   ├── css/
│   │   └── style.css      # Styles personnalisés
│   └── recordings/        # Dossier des enregistrements audio
├── templates/
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── register.html     # Inscription
│   ├── login.html        # Connexion
│   ├── record.html       # Interface d'enregistrement
│   ├── admin.html        # Tableau de bord admin
│   └── privacy.html      # Politique de confidentialité
├── pyproject.toml        # Dépendances Python
└── README.md            # Documentation
```

## 🛠️ Technologies utilisées

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM pour la base de données
- **Flask-Login** - Gestion des sessions utilisateur
- **Flask-WTF** - Protection CSRF
- **PostgreSQL** - Base de données relationnelle
- **Werkzeug** - Hachage sécurisé des mots de passe

### Frontend
- **Bootstrap 5** - Framework CSS responsive
- **HTML5 Audio API** - Enregistrement audio dans le navigateur
- **Jinja2** - Moteur de templates
- **CSS personnalisé** - Thème avec dégradés et animations

### Sécurité
- **CSRF Protection** - Protection contre les attaques CSRF
- **Password Hashing** - Hachage sécurisé des mots de passe
- **File Validation** - Validation des fichiers uploadés
- **Session Security** - Gestion sécurisée des sessions

## 🤝 Contribution

### Ajouter de nouvelles phrases

1. Éditez le fichier `phrases.txt`
2. Ajoutez une phrase par ligne en langue Rund
3. Redémarrez l'application pour charger les nouvelles phrases

### Développement

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Implémentez vos modifications
4. Testez soigneusement
5. Soumettez une pull request

## 🔒 Sécurité et confidentialité

### Protection des données

- **Consentement explicite** - Les utilisateurs doivent accepter la collecte de données
- **Hachage des mots de passe** - Aucun mot de passe n'est stocké en clair
- **Validation des fichiers** - Les uploads sont sécurisés et validés
- **Protection CSRF** - Tous les formulaires sont protégés

### Données collectées

- **Informations personnelles** : Nom, âge, sexe, lieu d'origine, email
- **Enregistrements audio** : Fichiers audio des prononciations
- **Métadonnées** : Dates d'enregistrement, phrases associées

### Droits des utilisateurs

- **Accès** : Consultation de leurs propres données
- **Rectification** : Modification des informations personnelles
- **Suppression** : Demande de suppression via l'administrateur

## 📞 Support

Pour toute question ou problème :
1. Consultez cette documentation
2. Vérifiez les logs de l'application
3. Contactez l'équipe de développement

---

**Note** : Cette application est conçue pour la préservation culturelle et la recherche académique. Traitez les données collectées avec le respect et la confidentialité qu'elles méritent.
