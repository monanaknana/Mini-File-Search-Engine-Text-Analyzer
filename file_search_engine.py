import os
import re
from PyPDF2 import PdfReader

import fitz  # PyMuPDF
import traceback


class FileSearchEngine:
    def __init__(self, file_path, search_term):
        self.file_path = file_path
        self.search_term = search_term

    def analyze_file(self):
        if not self.file_path or not os.path.isfile(self.file_path):
            return "Invalid file selected."

        if not self.search_term.strip():
            return "Search term cannot be empty."

        file_extension = os.path.splitext(self.file_path)[1].lower()

        if file_extension == ".txt":
            return self._analyze_text_file()
        elif file_extension == ".pdf":
            return self._analyze_pdf_file()
        else:
            return "Unsupported file format. Only .txt and .pdf files are supported."

    def _analyze_text_file(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.readlines()

            line_count = len(content)
            word_count = sum(len(line.split()) for line in content)
            term_count = sum(line.lower().count(self.search_term.lower()) for line in content)
            file_name = os.path.basename(self.file_path)

            result = [
                f"File: {file_name}",
                f"Total Lines: {line_count}",
                f"Total Words: {word_count}",
                f"Occurrences of '{self.search_term}': {term_count}",
                "",
                "Matching Lines:"
            ]

            for i, line in enumerate(content, start=1):
                if self.search_term.lower() in line.lower():
                    result.append(f"Line {i}: {line.strip()}")
                    result.append("")

            return "\n".join(result)

        except Exception as e:
            return f"An error occurred: {e}"

    def _analyze_pdf_file(self):
        try:
            reader = PdfReader(self.file_path)
            content = []

            # Extract text from all pages
            for page in reader.pages:
                content.append(page.extract_text())

            content = "\n".join(content).split("\n")
            line_count = len(content)
            word_count = sum(len(line.split()) for line in content)
            term_count = sum(line.lower().count(self.search_term.lower()) for line in content)
            file_name = os.path.basename(self.file_path)

            result = [
                f"File: {file_name}",
                f"Total Lines: {line_count}",
                f"Total Words: {word_count}",
                f"Occurrences of '{self.search_term}': {term_count}",
                "",
                "Matching Lines:"
            ]

            for i, line in enumerate(content, start=1):
                if self.search_term.lower() in line.lower():
                    highlighted_line = re.sub(
                        f"(?i)({re.escape(self.search_term)})",
                        r"==\1==",
                        line
                    )
                    result.append(f"Line {i}: {highlighted_line.strip()}")
                    result.append("")
                    

            return "\n".join(result)

        except Exception as e:
            return f"An error occurred while processing the PDF: {e}"

    def generate_highlighted_pdf(self):
        try:
            if not os.path.exists(self.file_path):
                return "The specified file does not exist."

            # Open the PDF document
            doc = fitz.open(self.file_path)
            colors = [fitz.utils.getColor("pink"), fitz.utils.getColor("yellow")]
            matches_found = False

            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                matches = list(re.finditer(re.escape(self.search_term), page_text, re.IGNORECASE))

                print(f"[DEBUG] Page {page_num + 1}: Found {len(matches)} matches.")

                if not matches:
                    continue

                matches_found = True
                for i, match in enumerate(matches):
                    rects = page.search_for(match.group())
                    for rect in rects:
                        color = colors[i % len(colors)]
                        annot = page.add_highlight_annot(rect)
                        annot.set_colors(stroke=color)
                        annot.update()

            if not matches_found:
                print("[DEBUG] No matches found in the document.")
                return "No matches found to highlight."

            # Save in the same directory as the original file
            original_dir = os.path.dirname(self.file_path)
            original_name = os.path.basename(self.file_path)
            highlighted_name = original_name.replace(".pdf", "_highlighted.pdf")
            highlighted_file_path = os.path.join(original_dir, highlighted_name)

            doc.save(highlighted_file_path)
            doc.close()

            # Verify the file saved successfully
            if os.path.exists(highlighted_file_path):
                print(f"[DEBUG] Highlighted PDF saved at: {highlighted_file_path}")
                return highlighted_file_path
            else:
                print("[DEBUG] Failed to save the highlighted PDF.")
                return "Failed to save the highlighted PDF."

        except PermissionError as e:
            print(f"[DEBUG] Permission error: {e}")
            return f"Permission error: {e}"

        except Exception as e:
            print(f"[DEBUG] Exception occurred: {e}")
            traceback.print_exc()
            return f"An error occurred while generating the highlighted PDF: {e}"




