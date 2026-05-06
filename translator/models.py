import torch
from transformers import MBartForConditionalGeneration, AutoTokenizer
import logging
import sys
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranslationModel:
    """
    Singleton pour charger et gérer le modèle de traduction mBART.
    Évite de recharger le modèle lourd (plusieurs Go) à chaque requête.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationModel, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        """Charge le modèle et le tokenizer depuis Hugging Face"""
        model_id = os.environ.get('TRANSLATION_MODEL_ID', 'eliezermga/ruund-translate')
        logger.info(f"📦 Chargement du modèle {model_id}...")
        
        try:
            import transformers
            # Supprimer les avertissements de chargement pour un log plus propre
            transformers.logging.set_verbosity_error()
            
            from transformers import MBartForConditionalGeneration, MBart50Tokenizer
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # 1. Charger le tokenizer de base
            # On utilise le base mBART-50 car on sait qu'il est compatible
            self.tokenizer = MBart50Tokenizer.from_pretrained("facebook/mbart-large-50")
            
            # 2. Ajouter le token spécial Ruund s'il n'existe pas
            if "ruu_CM" not in self.tokenizer.get_vocab():
                self.tokenizer.add_special_tokens({"additional_special_tokens": ["ruu_CM"]})
            
            self.src_lang = "ruu_CM"
            self.tgt_lang = "fr_XX"
            
            # 3. Charger le modèle
            # On utilise ignore_mismatched_sizes=True car le vocabulaire a été étendu
            self.model = MBartForConditionalGeneration.from_pretrained(
                model_id,
                ignore_mismatched_sizes=True
            ).to(self.device)
            
            # 4. S'assurer que le modèle est à la bonne taille de vocabulaire
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.model.eval()
            
            # Rétablir le logging normal
            transformers.logging.set_verbosity_info()
            logger.info("✅ Modèle chargé avec succès.")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle: {str(e)}")
            self.model = None
            self.tokenizer = None

    def translate(self, text, src_lang=None, tgt_lang=None):
        """Traduit le texte source vers la langue cible"""
        if self.model is None or self.tokenizer is None:
            return "Erreur: Modèle non chargé."

        src_code = src_lang if src_lang else self.src_lang
        tgt_code = tgt_lang if tgt_lang else self.tgt_lang

        try:
            # On définit la langue source
            self.tokenizer.src_lang = src_code
            
            encoded_input = self.tokenizer(text, return_tensors="pt", padding=True).to(self.device)
            
            # Récupération de l'ID du token de langue cible
            # On essaie d'abord via lang_code_to_id, sinon via convert_tokens_to_ids
            try:
                tgt_lang_id = self.tokenizer.lang_code_to_id[tgt_code]
            except (KeyError, AttributeError):
                tgt_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_code)

            generated_tokens = self.model.generate(
                **encoded_input,
                forced_bos_token_id=tgt_lang_id,
                max_length=128
            )
            
            translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            return translation
        except Exception as e:
            logger.error(f"❌ Erreur pendant la traduction: {str(e)}")
            return f"Erreur de traduction: {str(e)}"
