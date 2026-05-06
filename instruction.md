# 📘 Spécification Technique — LugaYetu (Web App)

## 1. Vue d’ensemble

**Nom du projet :** LugaYetu
**Type :** Application web
**Framework principal :** Django
**API :** Django REST Framework (DRF)
**Frontend :** Django Templates (consommant API interne)
**Base de données :** PostgreSQL
**Objectif principal :** Collecte de données linguistiques (texte + audio)

---

## 2. Contraintes globales

* Aucune fonctionnalité non spécifiée ne doit être implémentée
* Respect strict des bonnes pratiques Django (MVT)
* Code modulaire, maintenable, documenté
* Validation côté backend obligatoire
* Sécurité minimale requise (auth, CSRF, permissions)
* Toutes les actions critiques doivent être journalisées
* Application multilingue (FR / EN)
* Aucun texte en dur dans le code (utilisation i18n obligatoire)
* .env obligatoire pour les variables sensibles
* le theme doit s'adapter au parametre de l'utilisateur (clair, sombre, auto)
* avant d'ajouter un mot il faut se rassurer qu'il n'existe pas dans le locale
---

## 3. Stack technique imposée

### Backend

* Django
* Django REST Framework (API)
* PostgreSQL
* Gunicorn (serveur WSGI)
* Nginx (reverse proxy)

---

### Frontend

* Django Templates
* Tailwind CSS (design moderne)
* JavaScript natif (aucun framework frontend)

---

### Audio

* MediaRecorder API (navigateur)
* Format imposé : WAV
* Stockage : système de fichiers serveur (MEDIA_ROOT)

---

### Internationalisation (i18n)

* Django i18n system (`gettext`, `locale/`)
* Middleware : `LocaleMiddleware`
* Fichiers `.po` / `.mo`
* Langues supportées :

  * Français (`fr`)
  * Anglais (`en`)

---

### API

* Django REST Framework
* Authentification : Session + Token (DRF TokenAuth)
* Format : JSON uniquement

---

### Export

* CSV : bibliothèque standard Python
* ZIP : `zipfile`

---

## 4. Architecture du système

### 4.1 Modules principaux

* `accounts`
* `languages`
* `sentences`
* `recordings`
* `translator`
* `dashboard`
* `api` (centralisation endpoints DRF)

---

## 5. Modélisation des données

### 5.0 Règles générales

* Toutes les tables utilisent un **UUID comme clé primaire**
* Tous les champs texte sont en UTF-8 (support multilingue)
* Les relations utilisent `on_delete=CASCADE` sauf indication contraire
* Les champs sensibles sont validés côté backend
* Tous les modèles incluent :

  * `created_at`
  * `updated_at`

---

## 5.1 User (Custom User Model)

### Description

Modèle utilisateur principal basé sur `AbstractBaseUser` + `PermissionsMixin`

### Champs

* `id` : UUID (PK)
* `full_name` : CharField(max_length=255)
* `age` : IntegerField
* `language` : ForeignKey → Language
* `province` : CharField(max_length=255)
* `is_approved` : BooleanField (default=False)
* `is_active` : BooleanField (default=True)
* `is_staff` : BooleanField (admin Django)
* `date_joined` : DateTimeField
* `created_at` : DateTimeField
* `updated_at` : DateTimeField

### Contraintes

* `age > 10`
* utilisateur non approuvé ne peut pas utiliser l’application

---

## 5.2 Language

### Description

Liste des langues disponibles dans la plateforme

### Champs

* `id` : UUID (PK)
* `name` : CharField(max_length=100)
* `code` : CharField(max_length=10, unique=True)

### Contraintes

* `code` unique (ex: "fr", "en", "rw")

---

## 5.3 Sentence

### Description

Phrases à lire ou traduire

### Champs

* `id` : UUID (PK)
* `text` : TextField
* `language` : ForeignKey → Language
* `is_active` : BooleanField (default=True)
* `created_at`
* `updated_at`

### Contraintes

* texte non vide
* combinaison `(text, language)` unique

---

## 5.4 Recording

### Description

Enregistrements audio associés à une phrase

### Champs

* `id` : UUID (PK)
* `user` : ForeignKey → User
* `sentence` : ForeignKey → Sentence
* `audio_file` : FileField (upload_to="recordings/")
* `duration` : FloatField
* `is_validated` : BooleanField (default=False)
* `created_at`
* `updated_at`

### Contraintes

* durée ∈ [2, 20] secondes
* fichier obligatoire
* un utilisateur ne peut pas enregistrer deux fois la même phrase :

```id="kdbq1r"
UNIQUE(user, sentence)
```

---

## 5.5 Translation

### Description

Relation de traduction entre deux phrases existantes

### Champs

* `id` : UUID (PK)
* `source_sentence` : ForeignKey → Sentence (related_name="source_translations")
* `target_sentence` : ForeignKey → Sentence (related_name="target_translations")
* `created_at`
* `updated_at`

### Contraintes

* `source_sentence.language != target_sentence.language`
* unicité :

```id="i6r88v"
UNIQUE(source_sentence, target_sentence)
```

---

## 5.6 Indexation (OBLIGATOIRE)

### Index à créer

* `Sentence(language)`
* `Recording(user)`
* `Recording(sentence)`
* `Translation(source_sentence)`
* `Translation(target_sentence)`

---

## 5.7 Intégrité référentielle

* Suppression utilisateur → supprime ses enregistrements
* Suppression phrase → supprime enregistrements liés
* Suppression langue → interdite si utilisée (`PROTECT` recommandé)

---

## 5.8 Validation métier (Backend)

### User

* âge valide
* compte approuvé pour accès

---

### Recording

* vérifier durée réelle du fichier
* vérifier format `.wav`

---

### Sentence

* nettoyage texte (trim, normalisation)

---

## 5.9 Représentation Django (extrait)

```python id="2yqg8s"
class Recording(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    sentence = models.ForeignKey("sentences.Sentence", on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="recordings/")
    duration = models.FloatField()
    is_validated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "sentence")
```

---

## 5.10 Extensions interdites

NE PAS ajouter :

* champs inutiles (bio, avatar, etc.)
* relations non définies
* tables supplémentaires (EXCEPTION : Les tables servant à gérer le contenu texte dynamique depuis l'admin sont autorisées)

---



## 6. API REST (OBLIGATOIRE)

### 6.1 Règles globales

* Toutes les données doivent être accessibles via API
* Les vues templates doivent consommer ces APIs
* Permissions strictes par endpoint
* Format JSON uniquement

---

### 6.2 Endpoints

#### Authentification

* `POST /api/register/`
* `POST /api/login/`
* `POST /api/logout/`

---

#### Utilisateur

* `GET /api/profile/`
* `PUT /api/profile/`
* `DELETE /api/profile/`

---

#### Langues

* `GET /api/languages/`

---

#### Phrases

* `GET /api/sentences/random/`
  → retourne une phrase non encore enregistrée

---

#### Enregistrements

* `POST /api/recordings/`
* `GET /api/recordings/me/`
* `DELETE /api/recordings/{id}/`

---

#### Traduction

* `POST /api/translate/`

Input :

```
{
  "text": "...",
  "source_lang": "rw",
  "target_lang": "fr"
}
```

Output :

```
{
  "translation": "...",
  "status": "found | not_found"
}
```

---


## 7. Gestion multilingue (OBLIGATOIRE)

### 7.1 Backend

* Utiliser `gettext_lazy` pour tous les textes fixes (ex: boutons, menus, labels courts)
* Les textes dynamiques (paragraphes, titres de page) doivent provenir de la base de données (modifiables par l'admin en FR et EN)
* Aucun string affiché directement

---

### 7.2 Frontend

* `{% trans "..." %}` obligatoire
* `{% blocktrans %}` pour textes dynamiques

---

### 7.3 Configuration

```python
LANGUAGES = [
    ('fr', 'French'),
    ('en', 'English'),
]

LOCALE_PATHS = [BASE_DIR / "locale"]
```

---

## 8. Sécurité

* CSRF activé
* Validation fichiers audio (type + taille)
* Permissions DRF :

  * IsAuthenticated
  * IsAdminUser
* Vérification `is_approved` à chaque requête critique

---

## 9. Journalisation (Logging)

* Utiliser module `logging`
* Log obligatoire pour :

  * inscription
  * approbation utilisateur
  * upload audio
  * suppression données

---

## 10. Tests

* Django TestCase
* Tests API (DRF APITestCase)
* Validation formulaires

---

## 11. Déploiement

* OS : Linux
* Gunicorn
* Nginx
* PostgreSQL
* Collectstatic obligatoire

---

## 12. Non-objectifs (STRICT)

NE PAS implémenter :

* IA de traduction avancée
* Modèle ML
* Chatbot
* Notifications temps réel
* WebSocket
* Application mobile native

---

## 13. Flux utilisateur

### Contributeur
1. Inscription 
2. Attente validation 
3. Connexion 
4. Enregistrement audio 
5. Validation 
6. Consultation historique 
--- 
### Administrateur 
1. Connexion 
2. Validation utilisateurs 
3. Suivi statistiques 
4. Export données

---

## 14. Critères de réussite

* Données exploitables pour NLP 
* Interface simple et stable 
* Aucun bug critique 
* Export fonctionnel

---

## 15. Priorité de développement

1. Modèles + PostgreSQL
2. API DRF
3. Authentification
4. Enregistrement audio
5. Attribution phrases
6. Admin djazmin
7. UI

---

## 17. Frontend (HTML, CSS, JS) — Architecture et Bonnes Pratiques

### 17.1 Principes généraux

* Le frontend est basé sur **Django Templates**
* Le rendu HTML est **server-side**
* Le JavaScript est utilisé uniquement pour :

  * interactions UI
  * appels API
  * enregistrement audio (MediaRecorder)

---

### 17.2 Contraintes STRICTES

* ❌ Aucun texte en dur dans :

  * HTML
  * JavaScript
  * attributs (placeholder, title, etc.)

* ✅ Tous les textes doivent passer par :

  * `{% trans %}` ou `{% blocktrans %}`

---

## 17.3 Structure des fichiers

Organisation obligatoire :

```
templates/
    base/
        base.html
    components/
        navbar.html
        footer.html
        alerts.html
    pages/
        home.html
        login.html
        register.html
        dashboard.html
        record.html
        recordings.html
        translator.html

static/
    css/
        main.css
    js/
        main.js
        recorder.js
        api.js
    img/
```

---

## 17.4 HTML (Templates Django)

### Règles

* Utiliser **héritage de templates**

```html id="1l1zj4"
{% extends "base/base.html" %}
```

* Structure modulaire :

```html id="3v0lcz"
{% include "components/navbar.html" %}
```

---

### Traduction obligatoire

```html id="b6h7o3"
<h1>{% trans "Welcome" %}</h1>
```

Texte dynamique :

```html id="3u4h6k"
{% blocktrans %}Hello {{ user.full_name }}{% endblocktrans %}
```

---

### Interdictions

* Texte direct :

```html id="bad1"
<h1>Welcome</h1> ❌
```

---

## 17.5 CSS (Tailwind uniquement)

### Outil

* Tailwind CSS (via CDN ou build local)

---

### Règles

* Pas de CSS inline
* Pas de styles dans les templates (Les styles doivent être dans `static/css/main.css`)
* Support du mode sombre et clair via les classes Tailwind et JS (`static/js/main.js`)

❌ Interdit :

```html id="bad2"
<div style="color:red;"></div>
```

---

### Organisation

* `main.css` pour extensions globales uniquement
* Utiliser utilitaires Tailwind

---

## 17.6 JavaScript

### Structure

* `main.js` → logique globale
* `api.js` → appels API
* `recorder.js` → gestion audio

---

### Règles strictes

* Pas de logique métier complexe côté JS
* Toute validation critique doit être backend
* JS = couche d’interaction uniquement

---

### Interdiction de texte en dur

❌ Mauvais :

```javascript id="bad3"
alert("Recording saved");
```

✅ Correct :

```javascript id="good1"
alert(gettext("recording_saved"));
```

---

## 17.7 Internationalisation JS

### Outil

* Django JavaScript Catalog

### Configuration

```python id="cfg1"
path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog")
```

Dans template :

```html id="cfg2"
<script src="{% url 'javascript-catalog' %}"></script>
```

---

## 17.8 Appels API

### Règles

* Tous les appels passent par `api.js`
* Utiliser `fetch`

Exemple :

```javascript id="api1"
fetch("/api/recordings/", {
    method: "POST",
    body: formData,
    headers: {
        "X-CSRFToken": getCSRFToken()
    }
})
```

---

## 17.9 Gestion CSRF

* Token injecté via template Django
* Requis pour chaque requête POST/PUT/DELETE

---

## 17.10 Composants réutilisables

Créer composants :

* navbar
* footer
* messages (alerts)
* boutons standardisés

---

## 17.11 Accessibilité minimale

* labels pour inputs
* boutons explicites
* navigation clavier

---

## 17.12 Performance

* Minimiser JS
* Charger scripts en bas de page
* Utiliser `defer`

---

## 17.13 Sécurité frontend

* Ne jamais exposer logique sensible
* Ne jamais faire confiance au JS

---

## 17.14 Interdictions strictes

NE PAS :

* utiliser React / Vue / Angular
* injecter du HTML dynamique non contrôlé
* dupliquer logique backend
* écrire du texte directement dans JS ou HTML

---

## 17.15 Flux de rendu

1. Template Django rendu
2. Traductions injectées
3. JS chargé
4. Appels API exécutés

---

## 17.16 Résultat attendu

* Interface propre, modulaire
* Multilingue complet (FR / EN)
* Aucun texte en dur
* Séparation claire :

  * HTML = structure
  * CSS = style
  * JS = interaction

---

