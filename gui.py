import os
import re
from tkinter import filedialog, messagebox, ttk
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from file_search_engine import FileSearchEngine  # Ensure this file contains the necessary logic
import platform
import subprocess
import fitz  # PyMuPDF
import traceback

class FileSearchApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Mini File Search Engine & Text Analyzer")
        self.root.geometry("700x240")
        self.file_path = tk.StringVar()
        self.search_term = tk.StringVar()
        self.current_results = ""  # Store results for later reference

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = ctk.CTkFrame(self.root, fg_color="#9d000f", height=60)
        header_frame.pack(fill=tk.X)
        header_label = ctk.CTkLabel(
            header_frame,
            text="Mini File Search Engine & Text Analyzer",
            font=("Qanelas Soft", 18, "bold", "italic"),
            text_color="white"
        )
        header_label.pack(pady=10)

        # Main content frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white", corner_radius=15)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # File selection components
        ctk.CTkLabel(
            main_frame,
            text="Select File:",
            font=("Helvetica", 13, "bold"),
            text_color="black"
        ).grid(row=0, column=0, padx=10, pady=30, sticky="e")
        ctk.CTkEntry(
            main_frame,
            textvariable=self.file_path,
            font=("Helvetica", 12),
            height=30,
            width=350,
            corner_radius=10
        ).grid(row=0, column=1, padx=10, pady=10)
        browse_button = ctk.CTkButton(
            main_frame,
            text="Browse",
            command=self.browse_file,
            font=("Helvetica", 12, "bold"),
            fg_color="#9d000f",
            hover_color="#700008",
            text_color="white",
            corner_radius=10
        )
        browse_button.grid(row=0, column=2, padx=10, pady=10)

        # Search term input
        ctk.CTkLabel(
            main_frame,
            text="Search Term:",
            font=("Helvetica", 13, "bold"),
            text_color="black"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ctk.CTkEntry(
            main_frame,
            textvariable=self.search_term,
            font=("Helvetica", 12),
            height=30,
            width=350,
            corner_radius=10
        ).grid(row=1, column=1, padx=10, pady=10)
        search_button = ctk.CTkButton(
            main_frame,
            text="Search & Analyze",
            command=self.search_and_analyze,
            font=("Helvetica", 12, "bold"),
            fg_color="#9d000f",
            hover_color="#700008",
            text_color="white",
            corner_radius=10
        )
        search_button.grid(row=1, column=2, padx=10, pady=10)


    def browse_file(self):
        file = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("PDF Files", "*.pdf")]
        )
        if file:
            self.file_path.set(file)

    def search_and_analyze(self):
        file_path = self.file_path.get()
        search_term = self.search_term.get()

        if not file_path or not search_term:
            messagebox.showwarning("Input Error", "Please select a file and enter a search term.")
            return

        try:
            engine = FileSearchEngine(file_path, search_term)
            result = engine.analyze_file()

            # Extract summary and matching lines
            sections = result.split("\n\n")
            if len(sections) > 1:
                summary = sections[0]
                lines = "\n\n".join(sections[1:])
            else:
                summary = result
                lines = ""

            # Call method to display everything in the popup
            self.display_results_popup(summary, lines, search_term, file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_results_popup(self, summary, lines, search_term, file_path):
        """Creates a popup window displaying the summary table, results, and preview button."""
        popup = tk.Toplevel(self.root)
        popup.title("Search Results & Analysis")
        popup.geometry("800x500")

        # Summary Table Frame
        table_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=10)
        table_frame.pack(padx=10, pady=10, fill="x")

        summary_table = ttk.Treeview(
            table_frame,
            columns=("Metric", "Value"),
            show="headings",
            height=5
        )
        summary_table.heading("Metric", text="Main")
        summary_table.heading("Value", text="Detail")
        summary_table.column("Metric", width=200, anchor="w")
        summary_table.column("Value", width=400, anchor="center")
        summary_table.pack(fill="x", padx=10, pady=5)

        # Populate the Summary Table
        for line in summary.split("\n"):
            if ": " in line:
                metric, value = line.split(": ", 1)
                summary_table.insert("", "end", values=(metric, value))

        # Matching Lines Text Area
        result_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=10)
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)

        text_widget = tk.Text(
            result_frame,
            height=10,
            wrap="word",
            bg="#F9F9F9",
            fg="black",
            font=("Helvetica", 10)
        )
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)

        # Highlight occurrences of the search term
        text_widget.tag_config("highlight", background="yellow", foreground="black")
        text_widget.insert("1.0", lines)
        start_pos = "1.0"
        while True:
            start_idx = text_widget.search(search_term, start_pos, stopindex=tk.END, nocase=True)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(search_term)}c"
            text_widget.tag_add("highlight", start_idx, end_idx)
            start_pos = end_idx
        text_widget.config(state="disabled")

        # Buttons Frame: Align buttons side by side
        button_frame = ctk.CTkFrame(popup, fg_color="white")
        button_frame.pack(pady=10)

        preview_button = ctk.CTkButton(
            button_frame,
            text="Preview Highlights",
            command=lambda: self.preview_highlights(file_path, search_term),
            font=("Helvetica", 12, "bold"),
            fg_color="#9d000f",
            hover_color="#700008",
            text_color="white",
            corner_radius=10
        )
        preview_button.pack(side="left", padx=10)

        close_button = ctk.CTkButton(
            button_frame,
            text="Close",
            command=popup.destroy,
            font=("Helvetica", 12, "bold"),
            fg_color="#9d000f",
            hover_color="#700008",
            text_color="white",
            corner_radius=10
        )
        close_button.pack(side="left", padx=10)

    def preview_highlights(self, file_path, search_term):
            """Generate and preview highlighted PDF file."""
            if not file_path.endswith(".pdf"):
                messagebox.showwarning("Unsupported Format", "Highlight preview is only supported for PDF files.")
                return

            try:
                engine = FileSearchEngine(file_path, search_term)
                preview_file = engine.generate_highlighted_pdf()

                if preview_file and os.path.exists(preview_file):
                    if platform.system() == "Windows":
                        os.startfile(preview_file)
                    elif platform.system() == "Darwin":
                        subprocess.run(["open", preview_file])
                    else:
                        subprocess.run(["xdg-open", preview_file])
                else:
                    messagebox.showwarning("Preview Error", "Failed to create or open the highlighted PDF.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred during the preview: {e}")
    
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

    def run(self):
        self.root.mainloop()

