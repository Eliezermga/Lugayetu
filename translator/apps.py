from django.apps import AppConfig
import sys

class TranslatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translator'

    def ready(self):
        # On évite de charger le modèle lors des commandes comme 'migrate' ou 'collectstatic'
        if 'runserver' in sys.argv:
            # Import différé pour éviter les cycles
            from .models import TranslationModel
            # Pré-chargement du modèle au démarrage du serveur
            # TranslationModel() 
            pass
