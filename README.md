# Lugayetu - Plateforme de Préservation des Langues en Danger

![Lugayetu](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Description

**Lugayetu** est une application web Flask dédiée à la collecte, la préservation et la numérisation des langues en danger de la République Démocratique du Congo. Cette initiative scientifique et culturelle vise à sauvegarder le patrimoine linguistique congolais, notamment le **Rund**, le **Kisanga** et d'autres langues locales menacées de disparition.

### Mission

- 🎤 Collecter des enregistrements vocaux authentiques dans les langues en danger
- 📚 Créer un corpus linguistique pour la recherche scientifique
- 🌍 Préserver le patrimoine culturel et linguistique pour les générations futures
- 🔬 Faciliter le développement de technologies de traitement automatique de la parole

## ✨ Fonctionnalités

### Pour les Utilisateurs
- ✅ Inscription avec validation administrative
- 🎙️ Enregistrement vocal intuitif via navigateur (MediaRecorder API)
- 📝 Système de phrases aléatoires sans répétition
- 📊 Suivi du nombre d'enregistrements effectués
- 🔒 Connexion sécurisée avec authentification
- 👤 Modification du profil utilisateur (nom, email, mot de passe, etc.)
- 📁 Visualisation et téléchargement de ses enregistrements audio
- 🗑️ Suppression de compte avec tous les enregistrements associés

### Pour les Administrateurs
- 📈 Tableau de bord avec statistiques en temps réel
  - Nombre total d'utilisateurs approuvés
  - Utilisateurs en attente d'approbation
  - Nombre total d'enregistrements
  - Total d'heures enregistrées
  - Statistiques du jour
- 👥 Gestion complète des utilisateurs (approbation, rejet, suppression)
- 🎵 Gestion des enregistrements avec possibilité de suppression
- 📥 Export CSV avec métadonnées complètes
- 📦 Export ZIP (CSV + fichiers audio)
- 🌐 Gestion des langues (ajout/suppression)

### API REST Complète
- 🔌 API RESTful avec authentification JWT
- 📝 Documentation API complète (voir `API_DOCUMENTATION.md`)
- 🔄 Endpoints pour inscription, connexion, profil utilisateur
- 📊 Endpoints pour statistiques et gestion des enregistrements
- 🔐 Endpoints pour modification de profil et suppression de compte
- 📥 Endpoint pour téléchargement des fichiers audio
- 🌍 Support complet pour applications mobiles (React Native, Flutter)

### Fonctionnalités Techniques
- 🗄️ Base de données PostgreSQL pour la persistence
- 🔐 Authentification sécurisée avec Flask-Login et JWT
- 📱 Interface responsive avec Bootstrap 5
- 🎨 Design moderne et accessible
- 📄 Pages légales complètes (Politique de confidentialité, Conditions d'utilisation)
- 🔄 Migrations de base de données avec Flask-Migrate

## 🏗️ Architecture

```
lugayetu/
├── app.py                      # Application Flask principale
├── api.py                      # API REST avec JWT
├── models.py                   # Modèles de base de données
├── API_DOCUMENTATION.md        # Documentation complète de l'API
├── templates/                  # Templates HTML
│   ├── base.html              # Template de base
│   ├── index.html             # Page d'accueil
│   ├── register.html          # Inscription
│   ├── login.html             # Connexion
│   ├── record.html            # Interface d'enregistrement
│   ├── admin_dashboard.html   # Tableau de bord admin
│   ├── admin_users.html       # Gestion utilisateurs
│   ├── admin_languages.html   # Gestion langues
│   ├── privacy.html           # Politique de confidentialité
│   └── terms.html             # Conditions d'utilisation
├── static/
│   ├── css/
│   │   └── style.css          # Styles personnalisés
│   └── js/                    # Scripts JavaScript
├── uploads/
│   └── audio/                 # Fichiers audio enregistrés
├── languages/                 # Fichiers de phrases
│   ├── rund.txt              # Phrases en Rund
│   ├── translate_rund.txt    # Traductions françaises
│   └── ...                   # Autres langues
└── README.md                  # Documentation
```

## 🗄️ Modèles de Base de Données

### User (Utilisateur)
- **Informations personnelles** : nom, prénom, âge, sexe
- **Localisation** : province (26 provinces de la RDC), ville/village
- **Linguistique** : langue(s) parlée(s)
- **Authentification** : email, mot de passe hashé
- **Statut** : is_approved (validation admin), is_admin
- **Acceptation** : accepted_terms (conditions d'utilisation)

### Language (Langue)
- **Identification** : nom, code
- **Fichiers** : sentences_file, translations_file
- **Relations** : sentences (phrases associées)

### Sentence (Phrase)
- **Contenu** : text (texte dans la langue), translation (traduction)
- **Relations** : language_id, recordings (enregistrements)

### Recording (Enregistrement)
- **Associations** : user_id, sentence_id
- **Fichier** : audio_path
- **Métadonnées** : duration (durée en secondes), created_at

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.11+
- PostgreSQL
- Navigateur moderne supportant MediaRecorder API

### Installation

1. **Les dépendances sont déjà installées** :
   - Flask
   - Flask-SQLAlchemy
   - Flask-Login
   - Flask-Migrate (pour les migrations de base de données)
   - PostgreSQL (psycopg2-binary)
   - Pandas
   - Werkzeug
   - python-dotenv

2. **Configuration des variables d'environnement** :
   
   Copiez le fichier `.env.example` en `.env` et configurez les variables nécessaires :
   
   ```bash
   cp .env.example .env
   ```
   
   **Variables requises** (déjà configurées sur Replit) :
   - `DATABASE_URL` : URL de connexion PostgreSQL
   - `SESSION_SECRET` : Clé secrète pour les sessions Flask et JWT
   - `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` : Configuration PostgreSQL
   
   **Variables optionnelles** :
   - `UPLOAD_FOLDER` : Dossier de stockage des fichiers audio (par défaut: `uploads/audio`)
   - `MAX_CONTENT_LENGTH` : Taille maximale des fichiers en octets (par défaut: 52428800 = 50MB)

3. **Migration de la base de données** :
   
   Les migrations sont gérées avec Flask-Migrate (Alembic).
   
   **Pour un nouveau déploiement (base de données vide)** :
   ```bash
   # Appliquer toutes les migrations
   export FLASK_APP=app.py
   flask db upgrade
   ```
   
   **Pour modifier le schéma existant** :
   ```bash
   # Créer une migration après modification des modèles
   flask db migrate -m "Description des changements"
   
   # Appliquer la migration
   flask db upgrade
   ```
   
   **Note importante** : L'application utilise `db.create_all()` au démarrage pour garantir que la base de données est initialisée même sans migrations. Ceci est un mécanisme de compatibilité. Pour un environnement de production, il est recommandé d'utiliser uniquement les migrations (`flask db upgrade`).

4. **Démarrage automatique** :
   L'application démarre automatiquement via le workflow configuré.

### Configuration

#### Variables d'Environnement

Toutes les configurations sensibles sont gérées via des variables d'environnement pour une meilleure sécurité :

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL complète de connexion PostgreSQL | Requis |
| `SESSION_SECRET` | Clé secrète pour sessions et JWT | `lugayetu-secret-key-2024` |
| `UPLOAD_FOLDER` | Dossier des enregistrements audio | `uploads/audio` |
| `MAX_CONTENT_LENGTH` | Taille max fichiers (octets) | `52428800` (50MB) |

#### Compte Administrateur
- **Email** : `admin@lugayetu.cd`
- **Mot de passe** : `31082003` *(configuré dans le code)*

Le compte administrateur est créé automatiquement au premier démarrage.

### Accès à l'Application

L'application est accessible sur : **http://0.0.0.0:5000**

## 📝 Utilisation

### Pour les Contributeurs

1. **Inscription**
   - Accédez à la page d'inscription
   - Remplissez le formulaire avec vos informations :
     - Nom, prénom, âge, sexe
     - Langue(s) parlée(s)
     - Province (sélectionner parmi les 26 provinces)
     - Ville ou village
     - Email et mot de passe
   - Acceptez les conditions d'utilisation et la politique de confidentialité
   - Soumettez votre inscription

2. **Attente d'Approbation**
   - Votre inscription sera examinée par un administrateur
   - Vous recevrez une confirmation une fois approuvé

3. **Connexion et Enregistrement**
   - Connectez-vous avec votre email et mot de passe
   - Une phrase aléatoire s'affiche avec sa traduction
   - Cliquez sur "Enregistrer" pour commencer
   - Lisez la phrase clairement
   - Cliquez sur "Arrêter" pour terminer
   - Écoutez votre enregistrement
   - Validez ou réenregistrez si nécessaire
   - Une nouvelle phrase s'affiche après validation

### Pour les Administrateurs

1. **Connexion**
   - Email : `admin@lugayetu.cd`
   - Mot de passe : `31082003`

2. **Tableau de Bord**
   - Consultez les statistiques en temps réel
   - Visualisez les enregistrements récents
   - Exportez les données (CSV ou ZIP)

3. **Gestion des Utilisateurs**
   - Approuvez ou rejetez les nouvelles inscriptions
   - Visualisez tous les utilisateurs
   - Supprimez des comptes si nécessaire

4. **Gestion des Langues**
   - Ajoutez de nouvelles langues
   - Créez les fichiers de phrases correspondants
   - Supprimez des langues obsolètes

5. **Exports**
   - **Export CSV** : Téléchargez un fichier CSV avec toutes les métadonnées
     - ID Enregistrement, Nom Utilisateur, Sexe, Âge, Provenance
     - Email, Langue, Phrase, Traduction
     - Chemin Fichier Audio, Durée, Date
   - **Export ZIP** : Téléchargez un fichier ZIP contenant :
     - Le fichier CSV des métadonnées
     - Tous les fichiers audio

## 🌍 Provinces de la RDC

L'application supporte les 26 provinces de la République Démocratique du Congo :

- Kinshasa
- Kongo-Central
- Kwango, Kwilu, Mai-Ndombe
- Kasaï, Kasaï-Central, Kasaï-Oriental
- Lomami, Sankuru
- Maniema
- Sud-Kivu, Nord-Kivu
- Ituri
- Haut-Uélé, Bas-Uélé, Tshopo
- Tshuapa, Mongala
- Nord-Ubangi, Sud-Ubangi, Équateur
- Haut-Lomami, Lualaba
- Haut-Katanga, Tanganyika

## 🔄 Gestion des Migrations de Base de Données

### Qu'est-ce qu'une migration ?

Les migrations permettent de gérer les changements de schéma de base de données de manière contrôlée et versionnée. Chaque modification de la structure (ajout de table, de colonne, modification de type, etc.) est enregistrée dans un fichier de migration.

### Workflow de Migration

#### 1. Modifier les modèles
Éditez le fichier `models.py` pour ajouter, modifier ou supprimer des champs ou des tables.

#### 2. Créer une migration
```bash
export FLASK_APP=app.py
flask db migrate -m "Description claire des changements"
```

Cette commande génère automatiquement un fichier de migration dans `migrations/versions/` en comparant les modèles avec l'état actuel de la base de données.

#### 3. Vérifier la migration
Ouvrez le fichier de migration généré dans `migrations/versions/` et vérifiez que les changements sont corrects.

#### 4. Appliquer la migration
```bash
flask db upgrade
```

Cette commande applique les migrations en attente à la base de données.

### Commandes Utiles

```bash
# Voir l'historique des migrations
flask db history

# Revenir à la migration précédente
flask db downgrade

# Revenir à une migration spécifique
flask db downgrade <revision>

# Voir l'état actuel
flask db current

# Appliquer toutes les migrations
flask db upgrade head
```

### Exemple : Ajouter un champ à User

1. **Modifier `models.py`** :
```python
class User(UserMixin, db.Model):
    # ... champs existants ...
    phone = db.Column(db.String(20), nullable=True)  # Nouveau champ
```

2. **Créer la migration** :
```bash
flask db migrate -m "Add phone field to User model"
```

3. **Appliquer la migration** :
```bash
flask db upgrade
```

### Notes Importantes

- **Toujours créer une sauvegarde** avant d'appliquer des migrations en production
- **Tester les migrations** sur un environnement de développement d'abord
- **Ne jamais modifier** les fichiers de migration après qu'ils ont été appliqués
- Les migrations sont **automatiquement versionnées** avec Git

## 📚 Ajout de Nouvelles Langues

### Via l'Interface Admin

1. Connectez-vous en tant qu'administrateur
2. Accédez à "Gestion des langues"
3. Remplissez le formulaire :
   - **Nom** : Nom de la langue (ex: Kisanga)
   - **Code** : Code court en minuscules (ex: kisanga)
4. Cliquez sur "Ajouter"

### Ajout des Phrases

Après avoir ajouté une langue, créez deux fichiers dans le dossier `languages/` :

1. **`[code].txt`** : Une phrase par ligne dans la langue
2. **`translate_[code].txt`** : La traduction française correspondante

**Exemple** pour le Kisanga (`languages/kisanga.txt`) :
```
Mbote
Sango nini?
Nakozonga
```

**Traductions** (`languages/translate_kisanga.txt`) :
```
Bonjour
Comment allez-vous?
Je reviendrai
```

**Important** : Les deux fichiers doivent avoir le même nombre de lignes, chaque ligne correspondant à sa traduction.

## 🔒 Sécurité et Confidentialité

### Données Collectées
- Informations démographiques (nom, âge, sexe, localisation)
- Enregistrements vocaux
- Métadonnées des enregistrements

### Protection des Données
- Mots de passe hashés avec Werkzeug
- Sessions sécurisées avec Flask-Login
- Base de données PostgreSQL sécurisée
- Pages légales complètes

### Utilisation des Données
- Recherche scientifique en linguistique
- Préservation du patrimoine culturel
- Développement de technologies linguistiques
- Les données personnelles restent confidentielles

## 🛠️ Technologies Utilisées

### Backend
- **Flask** : Framework web Python
- **Flask-SQLAlchemy** : ORM pour PostgreSQL
- **Flask-Login** : Gestion des sessions utilisateurs
- **Flask-JWT-Extended** : Authentification JWT pour l'API
- **Flask-CORS** : Support CORS pour applications mobiles
- **Flask-Migrate** : Gestion des migrations de base de données (Alembic)
- **PostgreSQL** : Base de données relationnelle
- **Werkzeug** : Sécurité (hashage de mots de passe)
- **Pandas** : Génération de fichiers CSV
- **python-dotenv** : Gestion des variables d'environnement

### Frontend
- **HTML5/CSS3** : Structure et style
- **Bootstrap 5** : Framework CSS responsive
- **JavaScript ES6** : Logique côté client
- **MediaRecorder API** : Enregistrement audio dans le navigateur

### Déploiement
- **Replit** : Plateforme de développement et hébergement
- **Nix** : Gestionnaire de paquets

## 📊 Structure des Exports

### Format CSV
```csv
ID Enregistrement,Nom Utilisateur,Sexe,Âge,Provenance,Email,Langue,Phrase,Traduction,Chemin Fichier Audio,Durée (secondes),Date Enregistrement
1,Jean Kabongo,Homme,28,"Lubumbashi, Haut-Katanga",jean@example.com,Rund,Amahoro,Paix,uploads/audio/user1_sentence1_20241018_120530.webm,2.5,2024-10-18 12:05:30
```

### Format ZIP
```
lugayetu_complete_20241018_120530.zip
├── metadata.csv                           # Métadonnées complètes
└── user1_sentence1_20241018_120530.webm  # Fichiers audio
└── user2_sentence3_20241018_130245.webm
└── ...
```

## 🎯 Workflow d'Utilisation

### Pour un Contributeur
```
Inscription → Attente approbation → Connexion → Enregistrement vocal → 
Validation → Nouvelle phrase → Répétition → Contribution complète
```

### Pour un Administrateur
```
Connexion → Approbation utilisateurs → Consultation statistiques → 
Gestion enregistrements → Export données → Analyse scientifique
```

## 📈 Statistiques Disponibles

### Tableau de Bord
- 👥 Nombre total d'utilisateurs approuvés
- ⏰ Utilisateurs en attente d'approbation
- 🎤 Nombre total d'enregistrements
- ⏱️ Total d'heures enregistrées
- 📅 Enregistrements effectués aujourd'hui
- 📋 Liste des 10 enregistrements les plus récents

## 🤝 Contribution au Projet

Cette application est conçue pour un usage scientifique et culturel. Les contributions sont volontaires et non rémunérées. Chaque enregistrement aide à :

- Documenter des langues menacées
- Créer des ressources pour l'éducation
- Développer des outils technologiques pour les langues locales
- Préserver le patrimoine pour les générations futures

## 📞 Contact et Support

Pour toute question ou assistance :
- **Email** : eliezermunung@outlook.fr

## 📜 Licence et Droits

Les enregistrements vocaux sont sous licence ouverte pour la recherche scientifique et la préservation culturelle. Les contributeurs accordent une licence gratuite et perpétuelle d'utilisation de leurs enregistrements pour les finalités du projet.

## 🙏 Remerciements

Merci à tous les contributeurs qui participent à la préservation du patrimoine linguistique congolais. Votre voix compte pour sauvegarder ces langues pour les générations futures.

---

**Lugayetu** - *Ensemble, préservons notre héritage linguistique* 🇨🇩
