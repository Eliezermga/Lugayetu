import re

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
    
    print("=== ANALYSE DES PATTERNS DE RÉFÉRENCES ===")
    
    # Chercher tous les patterns potentiels
    motif_complet = rf'(?:#\s*)?(?:{pattern_livres})\s+[\d\s:;,]+\d+\s*\.'
    
    references = re.findall(motif_complet, contenu, re.MULTILINE)
    print(f"Nombre de références trouvées : {len(references)}")
    
    # Afficher les 20 premières pour analyse
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

def main():
    # Lecture du fichier
    with open('matthieu_aligné.txt', 'r', encoding='utf-8') as f:
        contenu = f.read()
    
    # Analyser d'abord
    livres = analyser_patterns(contenu)
    
    # Nettoyer
    resultat = nettoyer_references_final(contenu)
    
    # Sauvegarder
    with open('matthieu_nettoye_final.txt', 'w', encoding='utf-8') as f:
        f.write(resultat)
    
    print("\n=== STATISTIQUES ===")
    original_lines = len(contenu.split('\n'))
    nettoye_lines = len(resultat.split('\n'))
    print(f"Lignes originales : {original_lines}")
    print(f"Lignes nettoyées  : {nettoye_lines}")
    
    # Afficher les 20 premières lignes du résultat
    print("\n=== APERÇU DU RÉSULTAT (20 premières lignes) ===")
    for i, ligne in enumerate(resultat.split('\n')[:20]):
        print(f"{i+1:2d}: {ligne[:100]}...")

if __name__ == "__main__":
    main()