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
    Gestionnaire des modèles de traduction.
    Gère plusieurs modèles (Ruund->Français et Français->Ruund) en tant que Singletons.
    """
    _instances = {}

    def __new__(cls, model_type="ruu_fr"):
        model_id = os.environ.get('MODEL_RUU_FR', 'eliezermga/ruund-translate') if model_type == "ruu_fr" else os.environ.get('MODEL_FR_RUU', 'eliezermga/french-rund-translator')
        
        if model_id not in cls._instances:
            logger.info(f"Création d'une nouvelle instance pour {model_type} ({model_id})")
            instance = super(TranslationModel, cls).__new__(cls)
            instance.model_id = model_id
            instance.model_type = model_type
            instance._load_model()
            cls._instances[model_id] = instance
        return cls._instances[model_id]

    def _load_model(self):
        """Charge le modèle et le tokenizer depuis Hugging Face"""
        logger.info(f"Chargement du modèle {self.model_id}...")
        
        try:
            # Utiliser le token HF s'il est présent dans l'environnement
            hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
            logger.info(f"Token HF trouvé: {'Oui' if hf_token else 'Non'}")
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Utilisation du périphérique: {self.device}")
            
            # 1. Charger le tokenizer
            logger.info(f"Chargement du tokenizer pour {self.model_id}...")
            try:
                # On force fr_XX au début car ruu_CM n'est pas encore dans le vocabulaire
                # et mBART crashe à l'init s'il ne connaît pas la src_lang.
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_id, 
                    token=hf_token,
                    trust_remote_code=True,
                    src_lang="fr_XX"
                )
            except Exception as e:
                logger.warning(f"Erreur init tokenizer avec fr_XX: {e}")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_id, 
                    token=hf_token,
                    trust_remote_code=True
                )
            
            # S'assurer que le token ruu_CM est présent dans le vocabulaire
            if "ruu_CM" not in self.tokenizer.get_vocab():
                logger.info("Ajout du token 'ruu_CM' au vocabulaire...")
                self.tokenizer.add_special_tokens({"additional_special_tokens": ["ruu_CM"]})
            
            # Configuration mBART (lang_code_to_id est crucial pour mBART)
            if not hasattr(self.tokenizer, 'lang_code_to_id'):
                self.tokenizer.lang_code_to_id = {}
            
            # Forcer l'ID du token Ruund s'il n'est pas déjà mappé
            if "ruu_CM" not in self.tokenizer.lang_code_to_id:
                self.tokenizer.lang_code_to_id["ruu_CM"] = self.tokenizer.convert_tokens_to_ids("ruu_CM")

            # Définir les langues par défaut pour ce tokenizer
            if self.model_type == "ruu_fr":
                self.tokenizer.src_lang = "ruu_CM"
                self.tokenizer.tgt_lang = "fr_XX"
            else:
                self.tokenizer.src_lang = "fr_XX"
                self.tokenizer.tgt_lang = "ruu_CM"
            
            # 2. Charger le modèle
            logger.info(f"Chargement du modèle {self.model_id} (peut prendre du temps)...")
            self.model = MBartForConditionalGeneration.from_pretrained(
                self.model_id,
                token=hf_token,
                ignore_mismatched_sizes=True
            ).to(self.device)
            
            # 3. Ajuster le vocabulaire si nécessaire
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.model.eval()
            
            logger.info(f"Modèle {self.model_id} chargé avec succès.")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle {self.model_id}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            self.model = None
            self.tokenizer = None

    def translate(self, text, src_lang="ruu_CM", tgt_lang="fr_XX"):
        """Traduit le texte source vers la langue cible"""
        if self.model is None or self.tokenizer is None:
            return "Erreur: Modèle non chargé."

        try:
            # On définit la langue source sur le tokenizer
            self.tokenizer.src_lang = src_lang
            
            encoded_input = self.tokenizer(text, return_tensors="pt", padding=True).to(self.device)
            
            # Récupération de l'ID du token de langue cible
            try:
                tgt_lang_id = self.tokenizer.lang_code_to_id[tgt_lang]
            except (KeyError, AttributeError):
                tgt_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)

            generated_tokens = self.model.generate(
                **encoded_input,
                forced_bos_token_id=tgt_lang_id,
                max_length=128
            )
            
            translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            return translation
        except Exception as e:
            logger.error(f"Erreur pendant la traduction ({self.model_id}): {str(e)}")
            return f"Erreur de traduction: {str(e)}"
