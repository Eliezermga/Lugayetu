from django.apps import AppConfig
import sys
import logging

logger = logging.getLogger(__name__)

class TranslatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translator'

    def ready(self):
        # Ne pas charger le modèle pour les commandes de gestion qui ne nécessitent pas l'inférence.
        management_commands = {
            'migrate', 'makemigrations', 'collectstatic', 'test', 'shell',
            'dbshell', 'flush', 'loaddata', 'dumpdata', 'createsuperuser',
        }
        if len(sys.argv) > 1 and sys.argv[1] in management_commands:
            return

        # Pré-chargement du modèle au démarrage du worker, pour éviter le timeout Gunicorn
        try:
            from .models import TranslationModel
            logger.info('Préchargement des modèles de traduction Hugging Face au démarrage.')
            TranslationModel(model_type='ruu_fr')
            TranslationModel(model_type='fr_ruu')
        except Exception as e:
            logger.exception('Échec du préchargement du modèle de traduction : %s', e)
