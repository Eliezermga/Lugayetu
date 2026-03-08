# Lugayetu - Plateforme de Préservation des Langues en Danger

![Lugayetu](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Description

**Lugayetu** est une application web Flask dédiée à la collecte, la préservation et la numérisation des langues en danger de la République Démocratique du Congo, notamment le **Rund**, le **Kisanga** et d'autres langues locales.

### Mission

-  Collecter des enregistrements vocaux authentiques
-  Créer un corpus linguistique pour la recherche
-  Préserver le patrimoine culturel congolais
-  Faciliter le développement de technologies linguistiques

##  Fonctionnalités

### Utilisateurs
-  Inscription avec validation administrative
-  Enregistrement vocal via navigateur
-  Phrases aléatoires sans répétition
-  Gestion de profil (nom, âge, langue, province, mot de passe)
-  Visualisation et lecture de ses enregistrements
-  Suppression de compte

### Administrateurs
-  Tableau de bord avec statistiques temps réel
-  Gestion des utilisateurs (approbation, suppression)
-  Gestion des enregistrements
-  Export CSV et ZIP (métadonnées + audio)
-  Gestion des langues

### API REST
-  API RESTful avec JWT
-  Documentation complète : voir [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
-  Support mobile (React Native, Flutter)

##  Démarrage Rapide



### Accès
L'application est accessible sur : **http://0.0.0.0:5000**

##  Utilisation

### Contributeur
1. S'inscrire avec informations démographiques
2. Attendre l'approbation admin
3. Se connecter et enregistrer des phrases
4. Écouter et valider chaque enregistrement

### Administrateur
1. Se connecter avec le compte admin
2. Approuver les nouveaux utilisateurs
3. Consulter les statistiques
4. Exporter les données (CSV ou ZIP)


### Variables d'Environnement

| Variable | Description | Par défaut |
|----------|-------------|------------|
| `DATABASE_URL` | PostgreSQL URL | *Requis* |
| `SESSION_SECRET` | Clé sessions/JWT | `lugayetu-secret-key-2024` |
| `UPLOAD_FOLDER` | Dossier audio | `uploads/audio` |
| `MAX_CONTENT_LENGTH` | Taille max fichiers | `52428800` (50MB) |

### Migrations de Base de Données

```bash
# Appliquer les migrations
export FLASK_APP=app.py
flask db upgrade

# Créer une nouvelle migration
flask db migrate -m "Description"
```

##  Ajout de Langues

1. Via l'interface admin : "Gestion des langues"
2. Créer deux fichiers dans `languages/` :
   - `[code].txt` : phrases dans la langue
   - `translate_[code].txt` : traductions françaises

**Exemple** :
```
languages/kisanga.txt          languages/translate_kisanga.txt
-------------------            ---------------------------
Mbote                         Bonjour
Sango nini?                   Comment allez-vous?
```

##  Technologies

- **Backend** : Flask, PostgreSQL, Flask-Login, Flask-JWT, Flask-Migrate
- **Frontend** : Bootstrap 5, MediaRecorder API

##  Exports

### CSV
Métadonnées complètes : utilisateur, langue, phrase, traduction, durée, date

### ZIP
CSV + tous les fichiers audio

##  Sécurité

- Mots de passe hashés (Werkzeug)
- Sessions sécurisées (Flask-Login)
- Email non-modifiable
- Vérification de propriété des fichiers audio

##  Contact

**Email** : eliezermunung@outlook.fr

##  Licence

Licence ouverte pour la recherche scientifique et la préservation culturelle.

---

**Lugayetu** - *Ensemble, préservons notre héritage linguistique* 🇨🇩
