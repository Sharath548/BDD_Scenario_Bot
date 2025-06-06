import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.image_parser import extract_text_from_image
from parser.text_cleanup import clean_text
from parser.ollama_bdd_generator import generate_bdd_from_text
from parser.file_exporter import save_bdd_to_file

class TestScenarioBotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manual Test Scenario Bot")
        self.geometry("600x400")

        # File type selection
        self.file_type_label = tk.Label(self, text="Select file type:")
        self.file_type_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.file_type_var = tk.StringVar(value="pdf")
        self.file_type_combo = ttk.Combobox(self, textvariable=self.file_type_var, values=["pdf", "docx", "image"], state="readonly")
        self.file_type_combo.pack(fill="x", padx=10)

        # File selection
        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(self, textvariable=self.file_path_var)
        self.file_path_entry.pack(fill="x", padx=10, pady=(10, 0))

        self.browse_button = tk.Button(self, text="Browse File", command=self.browse_file)
        self.browse_button.pack(padx=10, pady=(0, 10))

        # Output format selection
        self.format_label = tk.Label(self, text="Select output format:")
        self.format_label.pack(anchor="w", padx=10)
        self.format_var = tk.StringVar(value="txt")
        self.format_combo = ttk.Combobox(self, textvariable=self.format_var, values=["txt", "md", "feature", "xlsx"], state="readonly")
        self.format_combo.pack(fill="x", padx=10, pady=(0, 10))

        # Generate button
        self.generate_button = tk.Button(self, text="Generate BDD Scenarios", command=self.generate_scenarios)
        self.generate_button.pack(pady=10)

        # Status text box
        self.status_text = tk.Text(self, height=8, state='disabled')
        self.status_text.pack(fill="both", expand=True, padx=10, pady=10)

    def browse_file(self):
        file_type = self.file_type_var.get()
        if file_type == 'pdf':
            filetypes = [("PDF files", "*.pdf")]
        elif file_type == 'docx':
            filetypes = [("Word documents", "*.docx")]
        else:
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]

        filename = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if filename:
            self.file_path_var.set(filename)

    def log(self, message):
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')

    def generate_scenarios(self):
        self.status_text.config(state='normal')
        self.status_text.delete('1.0', tk.END)
        self.status_text.config(state='disabled')

        file_type = self.file_type_var.get()
        file_path = self.file_path_var.get().strip()
        output_format = self.format_var.get()

        if not file_path:
            messagebox.showerror("Error", "Please select an input file.")
            return

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File does not exist.")
            return

        self.log(f"Extracting text from {file_type} file...")

        try:
            if file_type == 'pdf':
                text = extract_text_from_pdf(file_path)
            elif file_type == 'docx':
                text = extract_text_from_docx(file_path)
            else:
                text = extract_text_from_image(file_path)

            self.log(f"Raw text length: {len(text)} characters")

            text = clean_text(text)
            self.log(f"Cleaned text length: {len(text)} characters")

            self.log("Generating BDD scenarios...")
            bdd = generate_bdd_from_text(text)

            self.log("Saving scenarios...")
            output_path = save_bdd_to_file(bdd, output_format, file_path)

            messagebox.showinfo("Success", f"BDD scenarios saved:\n{output_path}")
            self.log(f"✅ Scenarios saved to: {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = TestScenarioBotGUI()
    app.mainloop()
