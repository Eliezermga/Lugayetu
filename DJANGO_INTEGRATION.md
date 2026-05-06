# Guide : Utiliser votre modèle mBART avec Django

## 📋 Table des matières
1. [Installation](#installation)
2. [Configuration Django](#configuration-django)
3. [Charger le modèle](#charger-le-modèle)
4. [Créer les endpoints](#créer-les-endpoints)
5. [Tester l'API](#tester-lapi)
6. [Déploiement en production](#déploiement-en-production)

---

## 1. Installation

### Prérequis
```bash
# Python 3.8+
python --version

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### Installer les packages
```bash
pip install django djangorestframework
pip install transformers torch
pip install python-decouple  # Pour les variables d'environnement
```

### Initialiser Django
```bash
django-admin startproject translation_project .
python manage.py startapp translator
```

---

## 2. Configuration Django

### `translation_project/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'translator',  # ← Ajouter votre app
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

# ⚠️ IMPORTANT : Configuration pour les modèles
import os
from decouple import config

# Réduire la verbosité des warnings transformers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Cache pour le modèle (optionnel mais recommandé)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
```

### `translation_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('translator.urls')),
]
```

---

## 3. Charger le modèle

### `translator/models.py` (ou create a new file)
```python
from django.db import models
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class TranslationModel:
    """Singleton pour charger le modèle une seule fois"""
    _instance = None
    _model = None
    _tokenizer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationModel, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
    
    def _load_model(self):
        """Charge le modèle et le tokenizer depuis Hugging Face"""
        print("📦 Chargement du modèle mBART...")
        
        model_id = "eliezermga/ruund-translate"
        
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(model_id)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
            
            # Utiliser GPU si disponible
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self._model.to(self.device)
            self._model.eval()  # Mode évaluation
            
            print(f"✅ Modèle chargé sur {self.device}")
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            raise
    
    @property
    def model(self):
        return self._model
    
    @property
    def tokenizer(self):
        return self._tokenizer
    
    def translate(self, text, src_lang="fr_XX", tgt_lang="en_XX", max_length=512):
        """
        Traduit un texte
        
        Args:
            text: Texte à traduire
            src_lang: Code langue source (fr_XX, en_XX, etc.)
            tgt_lang: Code langue cible
            max_length: Longueur maximale
        
        Returns:
            Texte traduit
        """
        try:
            # Formatter l'input avec les tokens de langue spéciaux
            formatted_text = f"{src_lang} {text}"
            
            # Tokenizer
            inputs = self._tokenizer(
                formatted_text,
                return_tensors="pt",
                max_length=max_length,
                truncation=True,
                padding=True
            )
            
            # Déplacer les inputs vers le bon device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Génération
            with torch.no_grad():
                outputs = self._model.generate(
                    **inputs,
                    forced_bos_token_id=self._tokenizer.convert_tokens_to_ids(tgt_lang),
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Décoder
            translation = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translation
        
        except Exception as e:
            print(f"❌ Erreur lors de la traduction: {e}")
            raise
```

### `translator/apps.py`
```python
from django.apps import AppConfig

class TranslatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translator'
    
    def ready(self):
        """Charge le modèle au démarrage de Django"""
        from .models import TranslationModel
        TranslationModel()  # Initialise le singleton
```

---

## 4. Créer les endpoints

### `translator/serializers.py`
```python
from rest_framework import serializers

class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000, required=True)
    src_lang = serializers.CharField(default="fr_XX", required=False)
    tgt_lang = serializers.CharField(default="en_XX", required=False)
    
    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Le texte ne peut pas être vide")
        return value
```

### `translator/views.py`
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TranslateSerializer
from .models import TranslationModel
import logging

logger = logging.getLogger(__name__)

class TranslateAPIView(APIView):
    """
    Endpoint pour traduire du texte
    
    POST /api/translate/
    {
        "text": "Bonjour le monde",
        "src_lang": "fr_XX",
        "tgt_lang": "en_XX"
    }
    """
    
    def post(self, request):
        serializer = TranslateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            model = TranslationModel()
            text = serializer.validated_data['text']
            src_lang = serializer.validated_data.get('src_lang', 'fr_XX')
            tgt_lang = serializer.validated_data.get('tgt_lang', 'en_XX')
            
            translation = model.translate(text, src_lang, tgt_lang)
            
            return Response({
                'original': text,
                'translation': translation,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Erreur de traduction: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckAPIView(APIView):
    """Vérifier que l'API est en ligne"""
    
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'API de traduction en ligne'
        }, status=status.HTTP_200_OK)
```

### `translator/urls.py`
```python
from django.urls import path
from .views import TranslateAPIView, HealthCheckAPIView

urlpatterns = [
    path('health/', HealthCheckAPIView.as_view(), name='health'),
    path('translate/', TranslateAPIView.as_view(), name='translate'),
]
```

---

## 5. Tester l'API

### Démarrer le serveur
```bash
python manage.py runserver
```

### Test avec curl
```bash
curl -X POST http://localhost:8000/api/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjour, comment allez-vous?",
    "src_lang": "fr_XX",
    "tgt_lang": "en_XX"
  }'
```

### Test avec Python
```python
import requests

url = "http://localhost:8000/api/translate/"
data = {
    "text": "Bonjour le monde",
    "src_lang": "fr_XX",
    "tgt_lang": "en_XX"
}

response = requests.post(url, json=data)
print(response.json())
```

### Test avec Postman
1. Créer une nouvelle requête POST
2. URL: `http://localhost:8000/api/translate/`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
  "text": "Bonjour",
  "src_lang": "fr_XX",
  "tgt_lang": "en_XX"
}
```

---

## 6. Déploiement en production

### Option 1 : Render.com (Recommandé) 🚀
```bash
# Créer requirements.txt
pip freeze > requirements.txt

# Créer Procfile
echo "web: gunicorn translation_project.wsgi:application" > Procfile

# Variables d'environnement sur Render:
# SECRET_KEY=votre_clé_secrète
# DEBUG=False
# ALLOWED_HOSTS=votre-domain.onrender.com
```

### Option 2 : Heroku
```bash
# Créer runtime.txt
echo "python-3.10.12" > runtime.txt

# Déployer
git push heroku main
```

### Option 3 : AWS EC2
```bash
# Sur une instance EC2 Ubuntu:
sudo apt-get update
sudo apt-get install python3-pip nginx

# Utiliser Gunicorn + Nginx comme reverse proxy
pip install gunicorn
gunicorn translation_project.wsgi:application --bind 0.0.0.0:8000
```

### Variables d'environnement (.env)
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,votre-domain.com
DATABASE_URL=postgres://user:password@localhost/db_name  # Si vous utilisez PostgreSQL
```

---

## 📝 Résumé des étapes

✅ Installer Django + transformers  
✅ Créer l'app `translator`  
✅ Charger le modèle HF dans un singleton  
✅ Créer les endpoints API  
✅ Tester localement  
✅ Déployer en production  

---

## 🔗 Codes de langue mBART

| Langue | Code |
|--------|------|
| Français | `fr_XX` |
| Anglais | `en_XX` |
| Espagnol | `es_XX` |
| Allemand | `de_DE` |
| Ruund | Dépend du code de votre modèle |

Consultez la [doc du modèle](https://huggingface.co/eliezermga/ruund-translate) pour les codes exacts.

---

## ⚡ Optimisations

### Caching des traductions
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 60)  # Cache 1 heure
def translate(request):
    # ...
```

### Batch processing
```python
def translate_batch(texts, src_lang="fr_XX", tgt_lang="en_XX"):
    model = TranslationModel()
    # Traiter plusieurs textes à la fois
    translations = []
    for text in texts:
        result = model.translate(text, src_lang, tgt_lang)
        translations.append(result)
    return translations
```

### Async avec Celery (pour requêtes longues)
```bash
pip install celery redis

# tasks.py
from celery import shared_task

@shared_task
def translate_async(text, src_lang, tgt_lang):
    model = TranslationModel()
    return model.translate(text, src_lang, tgt_lang)
```

---

## 📞 Support

- Docs Hugging Face: https://huggingface.co/docs
- Docs Django REST: https://www.django-rest-framework.org/
- Votre modèle: https://huggingface.co/eliezermga/ruund-translate
