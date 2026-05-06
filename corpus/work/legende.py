import fitz
from pathlib import Path


class ItalicTextExtractor:

    def __init__(self, input_folder, output_folder="captions"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)

    def extract_italic_text(self, pdf_path):

        doc = fitz.open(pdf_path)
        results = []

        for page_num, page in enumerate(doc):

            data = page.get_text("dict")

            for block in data["blocks"]:

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    for span in line["spans"]:

                        font = span["font"]
                        text = span["text"].strip()

                        if not text:
                            continue

                        # détecter italique
                        if "Italic" in font or "Oblique" in font:

                            results.append(
                                f"[Page {page_num+1}] {text}"
                            )

        doc.close()

        return results


    def process_pdf(self, pdf_path):

        print("Traitement :", pdf_path.name)

        captions = self.extract_italic_text(pdf_path)

        if captions:

            output = self.output_folder / f"{pdf_path.stem}_captions.txt"

            with open(output, "w", encoding="utf8") as f:

                for c in captions:
                    f.write(c + "\n")

            print(f"{len(captions)} textes italique extraits")

        else:

            print("aucun texte italique trouvé")


    def run(self):

        pdfs = list(self.input_folder.glob("*.pdf"))

        for pdf in pdfs:
            self.process_pdf(pdf)


if __name__ == "__main__":

    folder = input("Dossier PDF : ")

    extractor = ItalicTextExtractor(folder)

    extractor.run()