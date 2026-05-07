import os
import csv
import random
from django.conf import settings

def get_random_phrase_for_language(language_name):
    """
    Reads the TSV file for a given language and returns a random phrase.
    Format: {'phrase_native': '...', 'phrase_translation': '...'}
    """
    tsv_path = os.path.join(settings.BASE_DIR, 'data', 'languages', language_name, 'phrases.tsv')
    
    if not os.path.exists(tsv_path):
        return None
        
    phrases = []
    try:
        with open(tsv_path, 'r', encoding='utf-8') as f:
            # First, try to read with header
            reader = csv.reader(f, delimiter='\t')
            rows = list(reader)
            if not rows:
                return None
            
            header = rows[0]
            data_rows = rows[1:]
            
            # Identify column indices
            native_idx = -1
            trans_idx = -1
            
            for i, col in enumerate(header):
                col_lower = col.lower()
                if col_lower in ['phrase_native', 'native', 'original', 'ruund', language_name.lower()]:
                    native_idx = i
                elif col_lower in ['phrase_translation', 'translation', 'traduction', 'french', 'français', 'frenc']:
                    trans_idx = i
            
            # If not found by name, assume first two columns
            if native_idx == -1: native_idx = 0
            if trans_idx == -1: trans_idx = 1
            
            for row in data_rows:
                if len(row) > max(native_idx, trans_idx):
                    phrase_native = row[native_idx].strip()
                    phrase_trans = row[trans_idx].strip()
                    if phrase_native and phrase_trans:
                        phrases.append({
                            'phrase_native': phrase_native,
                            'phrase_translation': phrase_trans
                        })
    except Exception as e:
        print(f"Error reading TSV: {e}")
        return None
        
    if not phrases:
        return None
        
    return random.choice(phrases)


def get_total_phrase_count():
    """
    Returns the total number of phrase pairs across all language TSV files.
    """
    languages_dir = os.path.join(settings.BASE_DIR, 'data', 'languages')
    if not os.path.exists(languages_dir):
        return 0

    total = 0
    for lang_folder in os.listdir(languages_dir):
        tsv_path = os.path.join(languages_dir, lang_folder, 'phrases.tsv')
        if not os.path.exists(tsv_path):
            continue
        try:
            with open(tsv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter='\t')
                rows = list(reader)
                # Subtract 1 for the header row
                valid_rows = [r for r in rows[1:] if len(r) >= 2 and r[0].strip() and r[1].strip()]
                total += len(valid_rows)
        except Exception:
            pass

    return total
