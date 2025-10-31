# 🧪 Exemple pratique : Tester l'API avec Swagger UI

## 🎯 Objectif
Ce guide vous montre comment tester un endpoint complet de A à Z avec Swagger UI.

## 📝 Scénario : Créer un utilisateur et récupérer ses statistiques

### Étape 1 : Ouvrir Swagger UI

Allez sur : `http://votre-domaine/api-docs/`

Vous verrez tous les endpoints organisés par catégories.

---

### Étape 2 : Inscription d'un nouvel utilisateur

1. **Trouvez l'endpoint** : Cliquez sur la section **"Authentification"**
2. **Sélectionnez** : `POST /api//register`
3. **Cliquez** : Bouton **"Try it out"** (en haut à droite de l'endpoint)
4. **Modifiez le JSON** avec vos données :

```json
{
  "nom": "Mukendi",
  "prenom": "Grace",
  "age": 28,
  "sexe": "Femme",
  "langue_parlee": "Rund",
  "province": "Kinshasa",
  "ville_village": "Kinshasa",
  "email": "grace.mukendi@example.com",
  "password": "monmotdepasse123"
}
```

5. **Cliquez** : Bouton vert **"Execute"**
6. **Regardez la réponse** :

```json
{
  "success": true,
  "message": "Inscription réussie. Veuillez attendre l'approbation de l'administrateur.",
  "data": {
    "user_id": "user12",
    "email": "grace.mukendi@example.com",
    "is_approved": false
  }
}
```

✅ **Résultat** : Utilisateur créé avec succès !

---

### Étape 3 : Connexion

1. **Trouvez** : `POST /api//login` (dans "Authentification")
2. **Cliquez** : "Try it out"
3. **Entrez** : Utilisez vos identifiants

```json
{
  "email": "votre.email@example.com",
  "password": "votre_mot_de_passe"
}
```

4. **Cliquez** : "Execute"
5. **Copiez le token** dans la réponse :

```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY...",
    "user": {
      "id": 5,
      "user_id": "user5",
      "nom": "Mukendi",
      "prenom": "Grace",
      "email": "votre.email@example.com",
      "is_admin": false,
      "is_approved": true
    }
  }
}
```

✅ **Copiez** le `access_token` (tout le texte après "access_token": ")

---

### Étape 4 : S'authentifier dans Swagger

1. **En haut à droite**, cliquez sur le bouton vert **"Authorize" 🔓**
2. **Dans le popup**, entrez dans le champ :
   ```
   Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY...
   ```
   ⚠️ **N'oubliez pas** : Le mot "Bearer" + espace + votre token

3. **Cliquez** : "Authorize"
4. **Fermez** : Le popup

✅ Le cadenas 🔓 devient 🔒 - Vous êtes authentifié !

---

### Étape 5 : Obtenir les statistiques utilisateur

1. **Trouvez** : `GET /api//user/stats` (dans "Utilisateur")
2. **Cliquez** : "Try it out"
3. **Cliquez** : "Execute"
4. **Regardez la réponse** :

```json
{
  "success": true,
  "data": {
    "total_recordings": 6,
    "total_duration_seconds": 245.3,
    "total_duration_minutes": 4.09,
    "today_recordings": 0
  }
}
```

✅ **Résultat** : Vous voyez vos statistiques !

---

### Étape 6 : Lister les langues disponibles

1. **Trouvez** : `GET /api//languages` (dans "Langues")
2. **Cliquez** : "Try it out"
3. **Cliquez** : "Execute"
4. **Regardez la réponse** :

```json
{
  "success": true,
  "data": {
    "languages": [
      {
        "id": 1,
        "name": "Rund",
        "code": "rund",
        "total_sentences": 30
      }
    ]
  }
}
```

✅ **Résultat** : Liste complète des langues !

---

### Étape 7 : Obtenir une phrase à enregistrer

1. **Trouvez** : `GET /api//sentences/next` (dans "Phrases")
2. **Cliquez** : "Try it out"
3. **(Optionnel)** Filtrez par langue :
   - Dans le champ `language_id`, entrez : `1`
4. **Cliquez** : "Execute"
5. **Regardez la réponse** :

```json
{
  "success": true,
  "data": {
    "sentence": {
      "id": 15,
      "text": "Ngwami tonde ku mbuyi",
      "translation": "Je vais au marché",
      "language": {
        "id": 1,
        "name": "Rund",
        "code": "rund"
      }
    }
  }
}
```

✅ **Résultat** : Phrase prête à être enregistrée !

---

### Étape 8 : Lister mes enregistrements

1. **Trouvez** : `GET /api//recordings` (dans "Enregistrements")
2. **Cliquez** : "Try it out"
3. **(Optionnel)** Paramètres de pagination :
   - `page` : 1
   - `per_page` : 20
4. **Cliquez** : "Execute"
5. **Regardez la réponse** :

```json
{
  "success": true,
  "data": {
    "recordings": [
      {
        "id": 6,
        "duration": 4.5,
        "created_at": "2025-10-19T10:19:28",
        "sentence": {
          "id": 15,
          "text": "Ngwami tonde ku mbuyi",
          "translation": "Je vais au marché",
          "language": {
            "id": 1,
            "name": "Rund",
            "code": "rund"
          }
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 6,
      "pages": 1
    }
  }
}
```

✅ **Résultat** : Liste de tous vos enregistrements !

---

## 🎨 Fonctionnalités avancées de Swagger

### 📥 Télécharger un fichier audio

Pour tester `POST /api//recordings` :

1. **Cliquez** : "Try it out"
2. **Fichier audio** : 
   - Cliquez sur "Choose File"
   - Sélectionnez un fichier .wav, .mp3, .webm, etc.
3. **sentence_id** : Entrez l'ID de la phrase (ex: 15)
4. **duration** : Entrez la durée en secondes (ex: 5.3)
5. **Cliquez** : "Execute"

### 🔍 Filtrer les résultats

Plusieurs endpoints acceptent des paramètres de requête :

- `GET /api//sentences/next?language_id=1` - Filtrer par langue
- `GET /api//recordings?page=2&per_page=10` - Pagination

### 📝 Voir les exemples

Chaque endpoint affiche :
- **Request body** : Exemple de données à envoyer
- **Responses** : Exemples de réponses
- **Parameters** : Description de chaque paramètre

---

## 💡 Astuces

### ✅ Bonnes pratiques

1. **Toujours tester** `/login` en premier
2. **Copier le token** immédiatement après connexion
3. **S'authentifier** avant de tester les endpoints protégés
4. **Vérifier la réponse** : Code 200/201 = succès, 400/401/403/404/500 = erreur

### ⚠️ Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| 401 Unauthorized | Token manquant ou invalide | Cliquez sur "Authorize" et entrez "Bearer <token>" |
| 403 Forbidden | Compte non approuvé | Utilisez un compte admin ou approuvé |
| 404 Not Found | Endpoint incorrect | Vérifiez l'URL |
| 400 Bad Request | Données invalides | Vérifiez le format JSON |

### 🔄 Réinitialiser l'authentification

Pour tester avec un autre utilisateur :

1. Cliquez sur "Authorize"
2. Cliquez sur "Logout"
3. Connectez-vous avec un autre compte
4. Répétez le processus d'authentification

---

## 🎉 Félicitations !

Vous savez maintenant comment :
- ✅ Tester tous les endpoints
- ✅ S'authentifier avec JWT
- ✅ Envoyer des fichiers
- ✅ Filtrer les résultats
- ✅ Gérer les erreurs

**Continuez à explorer** les autres endpoints dans Swagger UI !
