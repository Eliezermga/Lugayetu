def verifier_sequence_fichier(nom_fichier):
    # On commence en s'attendant à trouver un 1
    nombre_attendu = 1
    erreurs_trouvees = 0

    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for numero_ligne, ligne in enumerate(fichier, start=1):
                # On sépare les mots de la ligne pour prendre le premier élément
                mots = ligne.strip().split()
                
                # Si la ligne est vide, on passe à la suivante
                if not mots:
                    continue
                
                try:
                    # On essaie de convertir le premier mot en nombre entier
                    nombre_actuel = int(mots[0])
                except ValueError:
                    # Si le premier mot n'est pas un nombre (ex: texte pur), on l'ignore
                    # Tu peux enlever le '#' ci-dessous si tu veux être averti de ces lignes
                    # print(f"Avertissement ligne {numero_ligne} : ne commence pas par un nombre.")
                    continue

                # Vérification de la logique de comptage
                if nombre_actuel == nombre_attendu:
                    # Tout est normal, on s'attend au prochain numéro pour la suite
                    nombre_attendu += 1
                    
                elif nombre_actuel == 1:
                    # Le comptage recommence à 1, c'est autorisé !
                    # La prochaine ligne devra donc être 2
                    nombre_attendu = 2
                    
                else:
                    # Il y a une erreur dans la séquence
                    print(f"Erreur à la ligne {numero_ligne} : attendu {nombre_attendu} (ou un redémarrage à 1), mais trouvé {nombre_actuel}.")
                    erreurs_trouvees += 1
                    
                    # On resynchronise le compteur avec le nombre actuel pour ne pas 
                    # déclencher de fausses erreurs sur toutes les lignes suivantes
                    nombre_attendu = nombre_actuel + 1
                    
        if erreurs_trouvees == 0:
            print("Parfait ! Aucune erreur de comptage n'a été trouvée dans le fichier.")
        else:
            print(f"Terminé. {erreurs_trouvees} erreur(s) trouvée(s) au total.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable. Vérifie le nom et l'emplacement.")

# --- COMMENT L'UTILISER ---
# Remplace 'mon_fichier.txt' par le vrai nom de ton fichier (et son chemin si nécessaire)
verifier_sequence_fichier('APOCfr_nettoye_aligné.txt')
