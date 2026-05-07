import os
import csv
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from core.models import Language

@receiver(post_save, sender=Language)
def create_language_resources(sender, instance, created, **kwargs):
    if created:
        # 1. Create audio directory: audio/Nom de la langue/
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio', instance.name)
        os.makedirs(audio_dir, exist_ok=True)
        
        # 2. Create language data directory: data/languages/Nom de la langue/
        data_dir = os.path.join(settings.BASE_DIR, 'data', 'languages', instance.name)
        os.makedirs(data_dir, exist_ok=True)
        
        # 3. Create TSV file: data/languages/Nom de la langue/phrases.tsv
        tsv_path = os.path.join(data_dir, 'phrases.tsv')
        if not os.path.exists(tsv_path):
            with open(tsv_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                # Header: phrase_native	phrase_translation
                writer.writerow(['phrase_native', 'phrase_translation'])
