# Documentation API Lugayetu

## Vue d'ensemble

Cette documentation décrit l'API REST de Lugayetu pour l'intégration avec des applications mobiles (React Native, Flutter, etc.) et des applications tierces.

### URL de base
```
https://votre-domaine.repl.co/api
```

### Authentification
L'API utilise des tokens JWT (JSON Web Tokens) pour l'authentification. Après connexion, vous recevrez un `access_token` qui doit être inclus dans toutes les requêtes protégées.

**Format du header d'authentification :**
```
Authorization: Bearer <access_token>
```

### Format des réponses
Toutes les réponses de l'API sont au format JSON avec la structure suivante :

**Succès :**
```json
{
  "success": true,
  "message": "Message descriptif",
  "data": {
    // Données de la réponse
  }
}
```

**Erreur :**
```json
{
  "success": false,
  "message": "Message d'erreur descriptif"
}
```

---

## Endpoints API

### 1. Inscription

Créer un nouveau compte utilisateur.

**Endpoint :** `POST /api/register`

**Authentification :** Non requise

**Corps de la requête :**
```json
{
  "nom": "Kasongo",
  "prenom": "Jean",
  "age": 25,
  "sexe": "Homme",
  "langue_parlee": "Rund",
  "province": "Kinshasa",
  "ville_village": "Kinshasa",
  "email": "jean.kasongo@example.com",
  "password": "motdepasse123"
}
```

**Champs requis :**
- `nom` (string) : Nom de famille
- `prenom` (string) : Prénom
- `age` (number) : Âge de l'utilisateur
- `sexe` (string) : "Homme", "Femme" ou "Autre"
- `langue_parlee` (string) : Langue parlée par l'utilisateur
- `province` (string) : Province de résidence (voir liste des provinces)
- `ville_village` (string) : Ville ou village
- `email` (string) : Adresse email unique
- `password` (string) : Mot de passe (minimum 6 caractères recommandé)

**Réponse réussie (201) :**
```json
{
  "success": true,
  "message": "Inscription réussie. Veuillez attendre l'approbation de l'administrateur.",
  "data": {
    "user_id": "user123",
    "email": "jean.kasongo@example.com",
    "is_approved": false
  }
}
```

**Erreurs possibles :**
- `400` : Champ manquant ou invalide
- `409` : Email déjà utilisé
- `500` : Erreur serveur

---

### 2. Connexion

Authentifier un utilisateur et obtenir un token d'accès.

**Endpoint :** `POST /api/login`

**Authentification :** Non requise

**Corps de la requête :**
```json
{
  "email": "jean.kasongo@example.com",
  "password": "motdepasse123"
}
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "message": "Connexion réussie",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 123,
      "user_id": "user123",
      "nom": "Kasongo",
      "prenom": "Jean",
      "email": "jean.kasongo@example.com",
      "is_admin": false,
      "is_approved": true
    }
  }
}
```

**Erreurs possibles :**
- `400` : Email ou mot de passe manquant
- `401` : Identifiants incorrects
- `403` : Compte non approuvé par l'administrateur
- `500` : Erreur serveur

---

### 3. Profil utilisateur

Obtenir les informations du profil de l'utilisateur connecté.

**Endpoint :** `GET /api/user/profile`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user123",
    "nom": "Kasongo",
    "prenom": "Jean",
    "age": 25,
    "sexe": "Homme",
    "langue_parlee": "Rund",
    "province": "Kinshasa",
    "ville_village": "Kinshasa",
    "email": "jean.kasongo@example.com",
    "is_approved": true,
    "created_at": "2025-10-18T10:30:00"
  }
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 4. Modifier le profil utilisateur

Mettre à jour les informations du profil de l'utilisateur connecté.

**Endpoint :** `PUT /api/user/profile`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Corps de la requête :**
```json
{
  "nom": "Nouveaunom",
  "prenom": "Nouveauprenom",
  "age": 26,
  "sexe": "Homme",
  "langue_parlee": "Rund",
  "province": "Kinshasa",
  "ville_village": "Kinshasa",
  "password": "nouveaumotdepasse"
}
```

**Champs modifiables (tous optionnels) :**
- `nom` (string) : Nouveau nom de famille
- `prenom` (string) : Nouveau prénom
- `age` (number) : Nouvel âge
- `sexe` (string) : "Homme", "Femme" ou "Autre"
- `langue_parlee` (string) : Nouvelle langue parlée
- `province` (string) : Nouvelle province (doit être dans la liste des provinces)
- `ville_village` (string) : Nouvelle ville ou village
- `password` (string) : Nouveau mot de passe

**Note :** L'email ne peut pas être modifié pour des raisons de sécurité.

**Note :** Vous pouvez envoyer uniquement les champs que vous souhaitez modifier.

**Réponse réussie (200) :**
```json
{
  "success": true,
  "message": "Profil mis à jour avec succès",
  "data": {
    "id": 123,
    "user_id": "user123",
    "nom": "Nouveaunom",
    "prenom": "Nouveauprenom",
    "age": 26,
    "sexe": "Homme",
    "langue_parlee": "Rund",
    "province": "Kinshasa",
    "ville_village": "Kinshasa",
    "email": "nouveau.email@example.com",
    "is_approved": true,
    "created_at": "2025-10-18T10:30:00"
  }
}
```

**Erreurs possibles :**
- `400` : Données invalides (âge non numérique, sexe invalide, province invalide)
- `401` : Token invalide ou expiré
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 5. Statistiques utilisateur

Obtenir les statistiques d'enregistrement de l'utilisateur.

**Endpoint :** `GET /api/user/stats`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "total_recordings": 45,
    "total_duration_seconds": 3245.5,
    "total_duration_minutes": 54.09,
    "today_recordings": 3
  }
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 6. Liste des langues

Obtenir toutes les langues disponibles dans l'application.

**Endpoint :** `GET /api/languages`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "languages": [
      {
        "id": 1,
        "name": "Rund",
        "code": "rund",
        "total_sentences": 150
      },
      {
        "id": 2,
        "name": "Kisanga",
        "code": "kisanga",
        "total_sentences": 200
      }
    ]
  }
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `500` : Erreur serveur

---

### 7. Prochaine phrase à enregistrer

Obtenir une phrase aléatoire non encore enregistrée par l'utilisateur.

**Endpoint :** `GET /api/sentences/next`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Paramètres de requête (optionnels) :**
- `language_id` : ID de la langue pour filtrer les phrases

**Exemples :**
```
GET /api/sentences/next
GET /api/sentences/next?language_id=1
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "sentence": {
      "id": 42,
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

**Réponse si toutes les phrases sont enregistrées :**
```json
{
  "success": true,
  "message": "Vous avez enregistré toutes les phrases disponibles",
  "data": {
    "sentence": null
  }
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 8. Sauvegarder un enregistrement

Envoyer un fichier audio enregistré pour une phrase.

**Endpoint :** `POST /api/recordings`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Corps de la requête (FormData) :**
- `audio` (file) : Fichier audio - Formats acceptés : WAV, WebM, MP3, OGG, M4A, AAC
- `sentence_id` (string) : ID de la phrase enregistrée
- `duration` (number) : Durée de l'enregistrement en secondes

**Formats audio supportés :**
- WAV (audio/wav, audio/wave)
- WebM (audio/webm) - Format par défaut pour l'enregistrement dans les navigateurs
- MP3 (audio/mpeg, audio/mp3)
- OGG (audio/ogg)
- M4A (audio/mp4)
- AAC (audio/aac)

**Exemple avec Axios (JavaScript) :**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.wav');
formData.append('sentence_id', '42');
formData.append('duration', '5.3');

axios.post('/api/recordings', formData, {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'multipart/form-data'
  }
});
```

**Réponse réussie (201) :**
```json
{
  "success": true,
  "message": "Enregistrement sauvegardé avec succès",
  "data": {
    "recording": {
      "id": 456,
      "duration": 5.3,
      "created_at": "2025-10-18T14:25:30"
    }
  }
}
```

**Erreurs possibles :**
- `400` : Fichier audio ou sentence_id manquant
- `401` : Token invalide ou expiré
- `404` : Phrase non trouvée
- `409` : Phrase déjà enregistrée par l'utilisateur
- `500` : Erreur serveur

---

### 9. Liste des enregistrements

Obtenir la liste paginée des enregistrements de l'utilisateur.

**Endpoint :** `GET /api/recordings`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Paramètres de requête (optionnels) :**
- `page` (number) : Numéro de page (défaut: 1)
- `per_page` (number) : Nombre d'éléments par page (défaut: 20, max: 100)

**Exemples :**
```
GET /api/recordings
GET /api/recordings?page=2&per_page=10
```

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "recordings": [
      {
        "id": 456,
        "duration": 5.3,
        "created_at": "2025-10-18T14:25:30",
        "sentence": {
          "id": 42,
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
      "total": 45,
      "pages": 3
    }
  }
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 10. Télécharger un fichier audio

Télécharger le fichier audio d'un enregistrement spécifique.

**Endpoint :** `GET /api/recordings/<recording_id>/audio`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**Paramètres d'URL :**
- `recording_id` : ID de l'enregistrement

**Exemple :**
```
GET /api/recordings/456/audio
```

**Réponse réussie (200) :**
Le fichier audio est téléchargé directement au format binaire avec les headers appropriés.

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `403` : Accès non autorisé (l'enregistrement appartient à un autre utilisateur)
- `404` : Enregistrement ou fichier audio non trouvé
- `500` : Erreur serveur

---

### 11. Supprimer le compte utilisateur

Supprimer définitivement le compte de l'utilisateur connecté ainsi que tous ses enregistrements et fichiers audio.

**Endpoint :** `DELETE /api/user/account`

**Authentification :** Requise

**Headers :**
```
Authorization: Bearer <access_token>
```

**⚠️ ATTENTION :** Cette action est irréversible. Toutes les données de l'utilisateur seront supprimées définitivement, y compris :
- Les informations du profil
- Tous les enregistrements audio
- Tous les fichiers audio associés

**Réponse réussie (200) :**
```json
{
  "success": true,
  "message": "Votre compte et tous vos enregistrements ont été supprimés avec succès"
}
```

**Erreurs possibles :**
- `401` : Token invalide ou expiré
- `403` : Impossible de supprimer un compte administrateur
- `404` : Utilisateur non trouvé
- `500` : Erreur serveur

---

### 12. Liste des provinces

Obtenir la liste des provinces de la RDC (endpoint public).

**Endpoint :** `GET /api/provinces`

**Authentification :** Non requise

**Réponse réussie (200) :**
```json
{
  "success": true,
  "data": {
    "provinces": [
      "Kinshasa",
      "Kongo-Central",
      "Kwango",
      "Kwilu",
      "Mai-Ndombe",
      "Kasaï",
      "Kasaï-Central",
      "Kasaï-Oriental",
      "Lomami",
      "Sankuru",
      "Maniema",
      "Sud-Kivu",
      "Nord-Kivu",
      "Ituri",
      "Haut-Uélé",
      "Bas-Uélé",
      "Tshopo",
      "Tshuapa",
      "Mongala",
      "Nord-Ubangi",
      "Sud-Ubangi",
      "Équateur",
      "Haut-Lomami",
      "Lualaba",
      "Haut-Katanga",
      "Tanganyika"
    ]
  }
}
```

---

## Codes d'erreur HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 201 | Ressource créée avec succès |
| 400 | Requête invalide (paramètres manquants ou incorrects) |
| 401 | Non authentifié (token manquant ou invalide) |
| 403 | Accès interdit (compte non approuvé) |
| 404 | Ressource non trouvée |
| 409 | Conflit (ressource déjà existante) |
| 500 | Erreur serveur interne |

---

## Exemple d'intégration React Native

### Installation des dépendances
```bash
npm install axios react-native-async-storage
```

### Configuration du client API

```javascript
// api/client.js
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://votre-domaine.repl.co/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token automatiquement
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Service d'authentification

```javascript
// services/authService.js
import apiClient from '../api/client';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const register = async (userData) => {
  const response = await apiClient.post('/register', userData);
  return response.data;
};

export const login = async (email, password) => {
  const response = await apiClient.post('/login', { email, password });
  if (response.data.success) {
    await AsyncStorage.setItem('access_token', response.data.data.access_token);
    await AsyncStorage.setItem('user', JSON.stringify(response.data.data.user));
  }
  return response.data;
};

export const logout = async () => {
  await AsyncStorage.removeItem('access_token');
  await AsyncStorage.removeItem('user');
};

export const getProfile = async () => {
  const response = await apiClient.get('/user/profile');
  return response.data;
};

export const getUserStats = async () => {
  const response = await apiClient.get('/user/stats');
  return response.data;
};
```

### Service d'enregistrement

```javascript
// services/recordingService.js
import apiClient from '../api/client';

export const getNextSentence = async (languageId = null) => {
  const url = languageId 
    ? `/sentences/next?language_id=${languageId}` 
    : '/sentences/next';
  const response = await apiClient.get(url);
  return response.data;
};

export const saveRecording = async (audioUri, sentenceId, duration) => {
  const formData = new FormData();
  
  formData.append('audio', {
    uri: audioUri,
    type: 'audio/wav',
    name: 'recording.wav',
  });
  formData.append('sentence_id', sentenceId.toString());
  formData.append('duration', duration.toString());

  const response = await apiClient.post('/recordings', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getRecordings = async (page = 1, perPage = 20) => {
  const response = await apiClient.get(`/recordings?page=${page}&per_page=${perPage}`);
  return response.data;
};

export const getLanguages = async () => {
  const response = await apiClient.get('/languages');
  return response.data;
};
```

### Exemple d'utilisation dans un composant

```javascript
// screens/RecordScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { getNextSentence, saveRecording } from '../services/recordingService';

const RecordScreen = () => {
  const [sentence, setSentence] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    loadNextSentence();
  }, []);

  const loadNextSentence = async () => {
    try {
      const response = await getNextSentence();
      if (response.success) {
        setSentence(response.data.sentence);
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de charger la phrase');
    }
  };

  const handleSaveRecording = async (audioUri, recordDuration) => {
    try {
      const response = await saveRecording(audioUri, sentence.id, recordDuration);
      if (response.success) {
        Alert.alert('Succès', 'Enregistrement sauvegardé !');
        loadNextSentence();
      }
    } catch (error) {
      Alert.alert('Erreur', 'Impossible de sauvegarder l\'enregistrement');
    }
  };

  return (
    <View>
      {sentence && (
        <>
          <Text style={{ fontSize: 20 }}>{sentence.text}</Text>
          <Text style={{ fontSize: 16, color: 'gray' }}>
            {sentence.translation}
          </Text>
        </>
      )}
    </View>
  );
};

export default RecordScreen;
```

---

## Gestion des erreurs

Il est recommandé de gérer les erreurs de manière centralisée :

```javascript
// api/errorHandler.js
export const handleApiError = (error) => {
  if (error.response) {
    // Le serveur a répondu avec un code d'erreur
    const { status, data } = error.response;
    
    switch (status) {
      case 401:
        // Token expiré, rediriger vers la page de connexion
        return 'Session expirée, veuillez vous reconnecter';
      case 403:
        return data.message || 'Accès non autorisé';
      case 404:
        return 'Ressource non trouvée';
      case 409:
        return data.message || 'Cette ressource existe déjà';
      case 500:
        return 'Erreur serveur, veuillez réessayer plus tard';
      default:
        return data.message || 'Une erreur est survenue';
    }
  } else if (error.request) {
    // La requête a été envoyée mais aucune réponse reçue
    return 'Pas de connexion internet';
  } else {
    // Autre erreur
    return 'Une erreur inattendue est survenue';
  }
};
```

---

## Notes importantes

1. **Sécurité** : Stockez le token JWT de manière sécurisée (AsyncStorage pour React Native)
2. **Expiration** : Les tokens expirent après 30 jours. Gérez le renouvellement ou la reconnexion
3. **Taille des fichiers** : La taille maximale des fichiers audio est de 50MB
4. **Formats audio** : L'API détecte automatiquement le format audio (WAV, WebM, MP3, OGG, M4A, AAC) et sauvegarde le fichier avec l'extension appropriée
5. **CORS** : L'API accepte les requêtes cross-origin pour faciliter l'intégration
6. **Encodage audio** : Pour React Native, utilisez le format WebM ou WAV pour une meilleure compatibilité

---

## Support

Pour toute question ou problème concernant l'API, contactez l'équipe de développement Lugayetu.

**Version de l'API :** 1.0  
**Dernière mise à jour :** 18 octobre 2025
