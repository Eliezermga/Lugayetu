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
            from transformers import MBartForConditionalGeneration, AutoTokenizer
            import transformers
            
            # Utiliser le token HF s'il est présent dans l'environnement
            hf_token = os.environ.get('HUGGING_FACE_HUB_TOKEN')
            logger.info(f"🔑 Token HF trouvé: {'Oui' if hf_token else 'Non'}")
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # 1. Charger le tokenizer
            logger.info("⏳ Chargement du tokenizer...")
            # On force une langue connue au début pour éviter le KeyError pendant l'init
            # si le fichier de config Hugging Face a 'ruu_CM' par défaut.
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id, 
                    token=hf_token,
                    trust_remote_code=True,
                    src_lang="fr_XX"
                )
            except Exception as e:
                logger.warning(f"⚠️ Erreur init tokenizer avec fr_XX, tentative sans src_lang: {e}")
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id, 
                    token=hf_token,
                    trust_remote_code=True
                )
            
            # S'assurer que le token ruu_CM est présent dans le vocabulaire
            if "ruu_CM" not in self.tokenizer.get_vocab():
                logger.info("➕ Ajout du token 'ruu_CM' au vocabulaire...")
                self.tokenizer.add_special_tokens({"additional_special_tokens": ["ruu_CM"]})
            
            # Enregistrement pour mBART (Fast et Slow)
            logger.info("📝 Enregistrement du code langue 'ruu_CM'...")
            
            # Pour le tokenizer Fast
            if hasattr(self.tokenizer, "_tokenizer"):
                # On peut parfois avoir besoin d'accéder au backend
                pass
                
            # Pour la compatibilité mBART
            if not hasattr(self.tokenizer, 'lang_code_to_id'):
                self.tokenizer.lang_code_to_id = {}
            
            self.tokenizer.lang_code_to_id["ruu_CM"] = self.tokenizer.convert_tokens_to_ids("ruu_CM")
            
            # Définir les langues par défaut
            self.src_lang = "ruu_CM"
            self.tgt_lang = "fr_XX"
            
            # Tester si on peut définir src_lang sur le tokenizer
            try:
                self.tokenizer.src_lang = "ruu_CM"
            except Exception as e:
                logger.warning(f"⚠️ Impossible de définir src_lang='ruu_CM' sur le tokenizer: {e}")
            
            # 2. Charger le modèle
            logger.info("⏳ Chargement du modèle (peut prendre du temps)...")
            self.model = MBartForConditionalGeneration.from_pretrained(
                model_id,
                token=hf_token,
                ignore_mismatched_sizes=True
            ).to(self.device)
            
            # 3. S'assurer que le modèle est à la bonne taille de vocabulaire
            self.model.resize_token_embeddings(len(self.tokenizer))
            self.model.eval()
            
            logger.info(f"✅ Modèle {model_id} chargé avec succès.")
        except Exception as e:
            logger.error(f"❌ Erreur CRITIQUE lors du chargement du modèle: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
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
