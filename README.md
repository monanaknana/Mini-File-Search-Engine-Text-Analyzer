# ITT440 - INDIVIDUAL PROJECT
NURUL IZZAH [CS2554B] |
ITT440 INDIVIDUAL PROJECT 

# File Search Engine & Text Analyzer

A Python-based project designed for managing and analyzing text data in `.txt` and `.pdf` files. This project combines a graphical user interface (GUI) with powerful text analysis and file search capabilities.

## Video Presentation
**https://youtu.be/LrVJZF44ZOg**

## Features

- **File Analysis**:
  - Supports `.txt` and `.pdf` file formats.
  - Displays file summary: total lines, words, and occurrences of specific search terms.
  - Highlights matching lines in real-time.

- **PDF Highlighting**:
  - Generates a highlighted version of the PDF with marked occurrences of the search term.
  - Opens the highlighted PDF for preview.

- **User Interface**:
  - Built with `tkinter` and `customtkinter`.
  - User-friendly interface for browsing files, entering search terms, and viewing results.
  - Styled for enhanced user experience (e.g., alternating row colors in tables).

- **Cross-Platform Support**:
  - Compatible with Windows, macOS, and Linux for PDF previews.

## Code Implementation

- **Core Functionality**:
  - File type detection and analysis.
  - PDF text extraction using `PyPDF2` and highlighting using `fitz` (PyMuPDF).
  - Regex-based search term highlighting.
  
- **File Structure**:
  - `file_search_engine.py`: Core functionality for file search and analysis.
  - `gui.py`: User interface design and logic.
  - `main.py`: Main entry point for launching the application.

## How to Use

1. **Launch the Application**:
   - Run `main.py` using Python 3.7 or later.
   
2. **Select a File**:
   - Click "Browse" to open a file selection dialog.
   - Choose a `.txt` or `.pdf` file.

3. **Analyze the File**:
   - Enter a search term in the input box.
   - Click "Search & Analyze" to process the file.
   - View results including file summary and highlighted matching lines.

4. **Preview Highlights** (for PDFs):
   - Click "Preview Highlights" to generate a highlighted PDF.
   - The highlighted PDF will open in your default viewer.

## Challenges and Solutions

- **Diverse File Formats**:
  - Modularized functions for `.txt` and `.pdf` files using specific libraries like `PyPDF2`.

- **Accurate Highlighting**:
  - Utilized `fitz` for precise text extraction and visual annotations.

- **Error Handling**:
  - Structured error handling for invalid files or empty search terms.

- **Cross-Platform Compatibility**:
  - Used platform-specific commands to ensure PDF preview functionality.

## Future Enhancements

- Expand file format support (e.g., `.docx`, `.xlsx`).
- Introduce advanced analytics like readability, keyword distribution, and sentiment analysis.
- Enable cloud integration with Google Drive or Dropbox.
- Optimize large PDF handling.
- Create a mobile-friendly version.
- Add dark mode, search history, and exportable analysis reports.

## System Requirements

- Python 3.7 or higher.
- Dependencies:
  - `PyPDF2`
  - `fitz` (PyMuPDF)
  - `customtkinter`

## Appendix

### Libraries Used
- `os`, `re`, `tkinter`, `customtkinter` for file handling and GUI.
- `PyPDF2` and `fitz` (PyMuPDF) for PDF processing.
- `subprocess` and `platform` for platform-specific functionality.
