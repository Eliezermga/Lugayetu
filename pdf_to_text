
import pytesseract
from pdf2image import convert_from_path
import re
import os

def extraction_sequentielle(texte, dernier_verset_connu, texte_en_attente):
    # Nettoyage initial et fusion du texte de la page
    texte = re.sub(r'-\s*\n', '', texte)
    texte = texte.replace('\n', ' ')
    
    # recherche des marqueurs de versets
    segments = re.split(r'(\d+|[?!$°#*]+)\s+', texte)
    
    resultat = []
    compteur = dernier_verset_connu
    # On commence avec le texte qui restait du PDF précédent
    buffer_actuel = texte_en_attente 
    
    # Si le texte commence pae du texte sans chiffre
    if segments[0].strip():
        buffer_actuel += " " + segments[0].strip()

    for i in range(1, len(segments), 2):
        marqueur = segments[i]
        contenu = segments[i+1].strip()
        
        if len(contenu) < 3: continue 
        
        try:
            valeur_lue = int(re.sub(r'\D', '', marqueur))
        except ValueError:
            valeur_lue = None

        # 
        if valeur_lue == compteur + 1 or valeur_lue is None or (valeur_lue > compteur and valeur_lue < compteur + 3):
            # enregistrement du verset en construction
            if buffer_actuel:
                resultat.append(f"{compteur} {buffer_actuel}")
            
            compteur += 1
            buffer_actuel = contenu
        else:
            # Sinon on considère que c'est la suite du texte
            buffer_actuel += " " + marqueur + " " + contenu

    return resultat, compteur, buffer_actuel

# --- CONFIGURATION ---
nom_du_dossier = 'le_nom_de_dossier_cible' 
output_file = f"{nom_du_dossier}_en_texte.txt"

pdf_files = sorted([f for f in os.listdir(nom_du_dossier) if f.lower().endswith('.pdf')])

verset_actuel = 1 # Modifier si besoin
reste_texte = ""   # stockage de le fin d\un pdf pour le suivant

print(f"lecture du dossier : {nom_du_dossier}")

with open(output_file, "w", encoding="utf-8") as f_final:
    for filename in pdf_files:
        path_pdf = os.path.join(nom_du_dossier, filename)
        print(f"\n[Fichier] {filename}")
        
        pages = convert_from_path(path_pdf, 300)
        
        for i, page in enumerate(pages):
            rw = pytesseract.image_to_string(page, lang='fra', config='--psm 1')
            
            lignes, verset_actuel, reste_texte = extraction_sequentielle(rw, verset_actuel, reste_texte)
            
            for l in lignes:
                f_final.write(l + "\n")
            
            print(f" Page {i+1} OK - Verset en cours : {verset_actuel}", end="\r")

    # ecriture du dernier morceau a ala fin
    if reste_texte:
        f_final.write(f"{verset_actuel} {reste_texte}\n")

print(f"\n\n operation terminee {output_file}.")
