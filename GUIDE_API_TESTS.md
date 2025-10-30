# 🚀 Guide d'utilisation de l'interface de test API Lugayetu

## 📋 Vue d'ensemble

Vous avez maintenant une interface de test API **similaire à Django REST Framework** grâce à Swagger UI !

## 🔗 Liens importants

- **Page d'accueil API** : `/api-home`
- **Interface Swagger UI** : `/api-docs/`
- **API v2 (documentée)** : `/api/v2/*`
- **API v1 (originale)** : `/api/*`

## 🎯 Comment tester l'API avec Swagger UI

### Étape 1 : Ouvrir Swagger UI

Allez sur : `votre-domaine/api-docs/`

Vous verrez une interface interactive avec tous vos endpoints organisés par catégories :
- 🔐 **Authentification** (Login, Register)
- 👤 **Utilisateur** (Profile, Stats)
- 🌍 **Langues** (Liste des langues)
- 📝 **Phrases** (Phrases à enregistrer)
- 🎙️ **Enregistrements** (Sauvegarder, Lister)
- 🌐 **Public** (Provinces)

### Étape 2 : Se connecter

1. Cliquez sur **POST /api/v2/login**
2. Cliquez sur le bouton **"Try it out"**
3. Modifiez le JSON avec vos identifiants :
   ```json
   {
     "email": "votre.email@example.com",
     "password": "votre_mot_de_passe"
   }
   ```
4. Cliquez sur **"Execute"**
5. Dans la réponse, **copiez le token** (access_token)

### Étape 3 : S'autoriser

1. En haut à droite de la page, cliquez sur le bouton vert **"Authorize" 🔓**
2. Dans le champ qui apparaît, entrez :
   ```
   Bearer votre_token_copié_ici
   ```
   ⚠️ **Important** : N'oubliez pas le mot "Bearer" suivi d'un espace !
   
3. Cliquez sur **"Authorize"**
4. Fermez la fenêtre

### Étape 4 : Tester les autres endpoints

Maintenant vous êtes authentifié ! Vous pouvez tester tous les endpoints :

#### 📊 Obtenir les statistiques utilisateur
- Cliquez sur **GET /api/v2/user/stats**
- Cliquez sur **"Try it out"**
- Cliquez sur **"Execute"**
- Vous verrez vos statistiques !

#### 🌍 Lister les langues disponibles
- Cliquez sur **GET /api/v2/languages**
- Cliquez sur **"Try it out"**
- Cliquez sur **"Execute"**

#### 📝 Obtenir la prochaine phrase
- Cliquez sur **GET /api/v2/sentences/next**
- Cliquez sur **"Try it out"**
- (Optionnel) Entrez un `language_id` pour filtrer
- Cliquez sur **"Execute"**

#### 🎙️ Sauvegarder un enregistrement
- Cliquez sur **POST /api/v2/recordings**
- Cliquez sur **"Try it out"**
- Remplissez les champs :
  - `audio` : Sélectionnez un fichier audio
  - `sentence_id` : ID de la phrase
  - `duration` : Durée en secondes
- Cliquez sur **"Execute"**

## 📝 Exemples de tests avec curl

### Login
```bash
curl -X POST "http://localhost:5000/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "votre.email@example.com",
    "password": "votre_mot_de_passe"
  }'
```

### Obtenir le profil (avec token)
```bash
curl -X GET "http://localhost:5000/api/v2/user/profile" \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

### Lister les provinces (endpoint public)
```bash
curl -X GET "http://localhost:5000/api/v2/provinces"
```

## 🔑 Authentification JWT

- **Token valide pendant** : 30 jours
- **Format du header** : `Authorization: Bearer <token>`
- **Où trouver le token** : Dans la réponse du endpoint `/login`

## 📊 Endpoints disponibles

### Public (sans authentification)
- `POST /api/v2/register` - Créer un compte
- `POST /api/v2/login` - Se connecter
- `GET /api/v2/provinces` - Liste des provinces

### Authentifié (avec token JWT)
- `GET /api/v2/user/profile` - Profil utilisateur
- `PUT /api/v2/user/profile` - Modifier le profil
- `GET /api/v2/user/stats` - Statistiques
- `GET /api/v2/languages` - Liste des langues
- `GET /api/v2/sentences/next` - Prochaine phrase
- `POST /api/v2/recordings` - Sauvegarder enregistrement
- `GET /api/v2/recordings` - Liste des enregistrements
- `DELETE /api/v2/user/account` - Supprimer le compte

## 🎨 Différences API v1 vs v2

### API v1 (`/api/*`)
- ✅ Fonctionnelle
- ❌ Pas de documentation Swagger
- ✅ Tous les endpoints disponibles

### API v2 (`/api/v2/*`)
- ✅ Fonctionnelle
- ✅ Documentation Swagger complète
- ✅ Interface de test interactive
- ✅ Même fonctionnalités que v1

**💡 Recommandation** : Utilisez l'API v2 pour profiter de l'interface de test Swagger !

## 🐛 Dépannage

### "Unauthorized" malgré le token
- Vérifiez que vous avez bien ajouté "Bearer " avant le token
- Assurez-vous que le token n'a pas expiré (30 jours)
- Reconnectez-vous pour obtenir un nouveau token

### "Try it out" ne fonctionne pas
- Actualisez la page Swagger
- Vérifiez que le serveur est bien démarré
- Consultez la console du navigateur pour les erreurs

### Fichier audio non accepté
- Formats acceptés : WAV, WebM, MP3, OGG, M4A, AAC
- Taille max : 50 MB
- Vérifiez que le champ `sentence_id` est bien rempli

## 📚 Ressources supplémentaires

- **Documentation complète** : `/API_DOCUMENTATION.md`
- **Scripts de test** : `test_api.sh` et `test_api_complete.sh`
- **Interface web** : `/` (pour l'interface utilisateur normale)

## 🎉 Félicitations !

Vous avez maintenant une interface de test API complète, similaire à Django REST Framework, pour tester et développer avec l'API Lugayetu !
