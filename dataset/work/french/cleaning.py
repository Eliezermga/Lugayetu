import re
import os

def analyser_patterns(contenu):
    """Analyse les patterns de références dans le fichier"""
    
    # Liste des livres bibliques (abréviations courantes)
    livres = [
        'Ge', 'Ex', 'Lé', 'No', 'De', 'Jos', 'Jg', 'Ru', '1 S', '2 S', '1 R', '2 R',
        '1 Ch', '2 Ch', 'Esd', 'Né', 'Est', 'Job', 'Ps', 'Pr', 'Ec', 'Ca', 'És', 'Jé',
        'La', 'Éz', 'Da', 'Os', 'Joë', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag',
        'Za', 'Mal', 'Mt', 'Mc', 'Lu', 'Jn', 'Ac', 'Ro', '1 Co', '2 Co', 'Ga', 'Ép',
        'Ph', 'Col', '1 Th', '2 Th', '1 Ti', '2 Ti', 'Tit', 'Phm', 'Hé', 'Ja', '1 Pi',
        '2 Pi', '1 Jn', '2 Jn', '3 Jn', 'Jude', 'Ap'
    ]
    
    # Trier par longueur décroissante pour matcher "1 Ch" avant "1"
    livres_trie = sorted(livres, key=len, reverse=True)
    pattern_livres = '|'.join(re.escape(l) for l in livres_trie)
    
    print("\n=== ANALYSE DES PATTERNS DE RÉFÉRENCES ===")
    
    # Chercher tous les patterns potentiels
    motif_complet = rf'(?:#\s*)?(?:{pattern_livres})\s+[\d\s:;,]+\d+\s*\.'
    
    references = re.findall(motif_complet, contenu, re.MULTILINE)
    print(f"Nombre de références trouvées : {len(references)}")
    
    # Afficher les 20 premières pour analyse
    if references:
        print("\nÉchantillon des 20 premières références :")
        for i, ref in enumerate(references[:20]):
            print(f"{i+1:2d}: {ref.replace(chr(10), '↵')}")
    
    return livres_trie

def nettoyer_references_final(contenu):
    """Nettoyage final avec tous les patterns identifiés"""
    
    # Liste complète des livres bibliques
    livres = [
        'Ge', 'Ex', 'Lé', 'No', 'De', 'Jos', 'Jg', 'Ru', '1 S', '2 S', '1 R', '2 R',
        '1 Ch', '2 Ch', 'Esd', 'Né', 'Est', 'Job', 'Ps', 'Pr', 'Ec', 'Ca', 'És', 'Jé',
        'La', 'Éz', 'Da', 'Os', 'Joë', 'Am', 'Ab', 'Jon', 'Mi', 'Na', 'Ha', 'So', 'Ag',
        'Za', 'Mal', 'Mt', 'Mc', 'Lu', 'Jn', 'Ac', 'Ro', '1 Co', '2 Co', 'Ga', 'Ép',
        'Ph', 'Col', '1 Th', '2 Th', '1 Ti', '2 Ti', 'Tit', 'Phm', 'Hé', 'Ja', '1 Pi',
        '2 Pi', '1 Jn', '2 Jn', '3 Jn', 'Jude', 'Ap'
    ]
    
    # Trier par longueur décroissante
    livres_trie = sorted(livres, key=len, reverse=True)
    pattern_livres = '|'.join(re.escape(l) for l in livres_trie)
    
    # Étape 1: Normaliser les retours à la ligne dans les références
    # Remplacer les retours à la ligne par des espaces pour faciliter le traitement
    contenu_normalise = contenu
    
    # Étape 2: Pattern pour capturer les références avec ou sans #
    # Capture: (optionnel #) + livre + espace + chiffres/séparateurs + point
    motif_reference = rf'(?:#\s*)?(?:{pattern_livres})\s+[\d\s:;,]+\d+\s*\.'
    
    # Étape 3: Remplacer chaque référence par un espace
    texte_nettoye = re.sub(motif_reference, ' ', contenu_normalise, flags=re.MULTILINE)
    
    # Étape 4: Nettoyer les références qui commencent par # mais sans espace après
    # Exemple: "fils de#Lu 1:31,32." -> "fils de."
    motif_hash = r'#\s*[A-Za-z0-9]+\s*[\d\s:;,]+\d+\s*\.'
    texte_nettoye = re.sub(motif_hash, ' ', texte_nettoye)
    
    # Étape 5: Nettoyer les cas particuliers de références multiples
    # Exemple: "#Ac 1:5; 11:16; 19:4."
    motif_multiple = r'#\s*[A-Za-z0-9]+\s*(?:[\d\s:;,]+\.?\s*)+'
    texte_nettoye = re.sub(motif_multiple, ' ', texte_nettoye)
    
    # Étape 6: Nettoyer les références sans # mais avec des chiffres
    # Pattern plus large pour capturer les références isolées
    motif_enhance = rf'(?:^|\s)(?:{pattern_livres})\s+[\d\s:;,]+\d+\s*\.(?=\s+[a-z])'
    texte_nettoye = re.sub(motif_enhance, ' ', texte_nettoye)
    
    # Étape 7: Normaliser les espaces multiples
    texte_nettoye = re.sub(r'[ \t]+', ' ', texte_nettoye)
    
    # Étape 8: Reconstruire les lignes proprement
    lignes = []
    for ligne in texte_nettoye.split('\n'):
        ligne = ligne.strip()
        # Garder les lignes non vides
        if ligne:
            # Nettoyer les espaces en trop à l'intérieur
            ligne = re.sub(r'\s+', ' ', ligne)
            lignes.append(ligne)
    
    return '\n'.join(lignes)

def obtenir_nom_fichier_sortie(chemin_entree):
    """Génère le nom du fichier de sortie"""
    dossier = os.path.dirname(chemin_entree)
    nom_fichier = os.path.basename(chemin_entree)
    
    # Séparer le nom et l'extension
    if '.' in nom_fichier:
        base, ext = nom_fichier.rsplit('.', 1)
        nom_sortie = f"{base}_nettoye.{ext}"
    else:
        nom_sortie = f"{nom_fichier}_nettoye"
    
    # Si un dossier est spécifié, y placer le fichier
    if dossier:
        return os.path.join(dossier, nom_sortie)
    else:
        return nom_sortie

def main():
    print("=== NETTOYEUR DE RÉFÉRENCES BIBLIQUES ===")
    print()
    
    # Demander le chemin du fichier à nettoyer
    while True:
        chemin_entree = input("Entrez le chemin du fichier à nettoyer : ").strip()
        
        # Supprimer les guillemets si présents (copier-coller de Windows)
        chemin_entree = chemin_entree.strip('"\'')
        
        if os.path.exists(chemin_entree):
            break
        else:
            print(f"Erreur : Le fichier '{chemin_entree}' n'existe pas.")
            print("Veuillez réessayer.\n")
    
    # Lecture du fichier
    try:
        with open(chemin_entree, 'r', encoding='utf-8') as f:
            contenu = f.read()
        print(f"\nFichier chargé : {chemin_entree}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return
    
    # Analyser les patterns
    livres = analyser_patterns(contenu)
    
    # Nettoyer
    print("\nNettoyage en cours...")
    resultat = nettoyer_references_final(contenu)
    
    # Générer le nom du fichier de sortie
    chemin_sortie = obtenir_nom_fichier_sortie(chemin_entree)
    
    # Sauvegarder
    try:
        with open(chemin_sortie, 'w', encoding='utf-8') as f:
            f.write(resultat)
        print(f"Résultat enregistré dans : {chemin_sortie}")
    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier : {e}")
        return
    
    print("\n=== STATISTIQUES ===")
    original_lignes = len(contenu.split('\n'))
    nettoye_lignes = len(resultat.split('\n'))
    original_caracteres = len(contenu)
    nettoye_caracteres = len(resultat)
    
    print(f"Lignes originales : {original_lignes}")
    print(f"Lignes nettoyées  : {nettoye_lignes}")
    print(f"Caractères originaux : {original_caracteres}")
    print(f"Caractères nettoyés  : {nettoye_caracteres}")
    print(f"Réduction : {original_caracteres - nettoye_caracteres} caractères")
    
    # Afficher les 20 premières lignes du résultat
    print("\n=== APERÇU DU RÉSULTAT (20 premières lignes) ===")
    lignes_resultat = resultat.split('\n')
    for i, ligne in enumerate(lignes_resultat[:20]):
        print(f"{i+1:2d}: {ligne[:100]}{'...' if len(ligne) > 100 else ''}")
    
    if len(lignes_resultat) > 20:
        print(f"... et {len(lignes_resultat) - 20} lignes supplémentaires")

if __name__ == "__main__":
    main()