import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationModel:
    """
    Mock du gestionnaire des modèles de traduction pour Render (basse ressource).
    Ce service est désactivé sur cette branche pour optimiser les performances.
    """
    _instances = {}

    def __new__(cls, model_type="ruu_fr"):
        if model_type not in cls._instances:
            instance = super(TranslationModel, cls).__new__(cls)
            instance.model_id = "mock"
            instance.model_type = model_type
            cls._instances[model_type] = instance
        return cls._instances[model_type]

    def translate(self, text, src_lang="ruu_CM", tgt_lang="fr_XX"):
        """Retourne un message d'indisponibilité"""
        return "Ce service n'est pas encore disponible sur cette plateforme."
