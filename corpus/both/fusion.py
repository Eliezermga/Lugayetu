import os


def read_txt(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split(' ', 1)

            if len(parts) != 2:
                print(f"[ERREUR FORMAT] Ligne {i} dans {file_path}")
                continue

            verse_id, text = parts
            data.append((i, verse_id.strip(), text.strip()))

    return data


def align_and_export(ruwund_file, francais_file, output_file):
    ruwund_data = read_txt(ruwund_file)
    francais_data = read_txt(francais_file)

    if len(ruwund_data) != len(francais_data):
        print("Nombre de lignes différent")
        print(f"Ruwund: {len(ruwund_data)}")
        print(f"Français: {len(francais_data)}")
        return

    print("Nombre de lignes identique")

    errors = 0

    with open(output_file, 'w', encoding='utf-8') as out:
        for i in range(len(ruwund_data)):
            _, verse_r, text_r = ruwund_data[i]
            _, verse_f, text_f = francais_data[i]

            if verse_r != verse_f:
                print(f"Incohérence à la ligne {i+1}")
                print(f"Ruwund: {verse_r}")
                print(f"Français: {verse_f}")
                errors += 1
                continue

            out.write(f"{verse_r}\t{text_r}\t{text_f}\n")

    if errors == 0:
        print(f"TSV généré : {output_file}")
    else:
        print(f"{errors} incohérence(s) détectée(s)")


def main():
    print("ALIGNEMENT Ruwund - Français")

    ruwund_file = input("Chemin du fichier Ruwund : ").strip()
    francais_file = input("Chemin du fichier Français : ").strip()
    output_file = input("Nom du fichier de sortie (.tsv) : ").strip()

    if not os.path.exists(ruwund_file):
        print(f"Fichier introuvable : {ruwund_file}")
        return

    if not os.path.exists(francais_file):
        print(f"Fichier introuvable : {francais_file}")
        return

    align_and_export(ruwund_file, francais_file, output_file)


if __name__ == "__main__":
    main()