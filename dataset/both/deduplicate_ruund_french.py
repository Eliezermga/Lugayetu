from collections import Counter
from pathlib import Path


INPUT_FILE = Path("dataset/both/ruund-french.tsv")
BACKUP_FILE = INPUT_FILE.with_suffix(INPUT_FILE.suffix + ".bak")


def main() -> None:
    lines = INPUT_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    normalized = [line.rstrip("\n") for line in lines]
    counts = Counter(normalized)

    duplicates = [(line, count) for line, count in counts.items() if count > 1]
    if not duplicates:
        print("Aucune ligne dupliquee trouvee.")
        return

    print("Lignes dupliquees detectees :")
    for line, count in duplicates:
        print(f"[x{count}] {line}")

    BACKUP_FILE.write_text("".join(lines), encoding="utf-8")

    seen = set()
    deduplicated_lines = []
    for line in lines:
        key = line.rstrip("\n")
        if key in seen:
            continue
        seen.add(key)
        deduplicated_lines.append(line)

    INPUT_FILE.write_text("".join(deduplicated_lines), encoding="utf-8")

    removed_count = len(lines) - len(deduplicated_lines)
    print()
    print(f"Sauvegarde creee : {BACKUP_FILE}")
    print(f"Lignes supprimees : {removed_count}")
    print(f"Lignes restantes : {len(deduplicated_lines)}")


if __name__ == "__main__":
    main()
