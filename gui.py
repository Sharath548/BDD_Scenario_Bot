import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import queue
import os
import logging

from parser.processing import process_file
from parser.processing import vector_store

cancel_flag = threading.Event()


# Custom log handler for logging into the Tkinter GUI
class TkinterLogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put((record.levelname, msg))


class TestScenarioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Scenario Generator")
        self.root.geometry("1000x850")

        self.selected_file = tk.StringVar()
        self.selected_format = tk.StringVar(value="txt")
        self.domain_choice = tk.StringVar(value="Retail")
        self.custom_prompt = tk.StringVar()
        self.generated_file_path = tk.StringVar()
        self.log_level_filter = tk.StringVar(value="ALL")

        self.log_queue = queue.Queue()

        self.dark_mode = False

        self.build_ui()
        self.setup_logger()
        self.bind_shortcuts()
        self.poll_log_queue()

    def build_ui(self):
        # Create main container with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # File selection
        ttk.Label(self.scrollable_frame, text="Select a file (PDF, DOCX, PNG, JPG, or code file):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Entry(self.scrollable_frame, textvariable=self.selected_file, width=80).grid(row=1, column=0, sticky="we", padx=10)
        ttk.Button(self.scrollable_frame, text="Browse", command=self.browse_file).grid(row=1, column=1, sticky="w", padx=5)

        # File format
        ttk.Label(self.scrollable_frame, text="Select output format:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        formats = ["txt", "md", "feature", "xlsx"]
        ttk.OptionMenu(self.scrollable_frame, self.selected_format, self.selected_format.get(), *formats).grid(row=3, column=0, sticky="w", padx=10)

        # Domain prompt tuning
        ttk.Label(self.scrollable_frame, text="Select domain:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        domains = ["Retail", "Banking", "Healthcare", "Ecommerce", "Code", "Custom"]
        domain_menu = ttk.OptionMenu(self.scrollable_frame, self.domain_choice, self.domain_choice.get(), *domains, command=self.toggle_custom_prompt)
        domain_menu.grid(row=5, column=0, sticky="w", padx=10)

        self.custom_prompt_entry = ttk.Entry(self.scrollable_frame, textvariable=self.custom_prompt, width=80)
        # Initially hidden, will be shown only if Custom is selected

        # Progress bar
        self.progress = ttk.Progressbar(self.scrollable_frame, orient="horizontal", length=500, mode="determinate")
        self.progress.grid(row=6, column=0, sticky="w", padx=10, pady=10)

        # Buttons
        btn_frame = ttk.Frame(self.scrollable_frame)
        btn_frame.grid(row=7, column=0, sticky="w", padx=10, pady=5, columnspan=3)

        self.generate_button = ttk.Button(btn_frame, text="Generate BDD Scenarios (Ctrl+G)", command=self.run_threaded)
        self.generate_button.grid(row=0, column=0, padx=5)
        self.cancel_button = ttk.Button(btn_frame, text="Cancel (Ctrl+C)", command=self.cancel_generation, state="disabled")
        self.cancel_button.grid(row=0, column=1, padx=5)
        self.copy_button = ttk.Button(btn_frame, text="Copy Preview to Clipboard", command=self.copy_preview)
        self.copy_button.grid(row=0, column=2, padx=5)
        self.dark_mode_button = ttk.Button(btn_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_button.grid(row=0, column=3, padx=5)

        # BDD Preview with scrollbar
        ttk.Label(self.scrollable_frame, text="BDD Scenario Preview:").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        preview_frame = ttk.Frame(self.scrollable_frame)
        preview_frame.grid(row=9, column=0, sticky="nsew", padx=10, pady=5)
        preview_scrollbar = ttk.Scrollbar(preview_frame)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bdd_preview = tk.Text(preview_frame, height=15, wrap="word", yscrollcommand=preview_scrollbar.set)
        self.bdd_preview.pack(fill=tk.BOTH, expand=True)
        preview_scrollbar.config(command=self.bdd_preview.yview)

        # Vector DB Search
        ttk.Label(self.scrollable_frame, text="Search Vector DB by tag:").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.tag_var = tk.StringVar()
        self.tag_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.tag_var, values=vector_store.get_tags())
        self.tag_menu.grid(row=11, column=0, sticky="w", padx=10)
        self.tag_menu.bind("<<ComboboxSelected>>", self.search_by_tag)

        # Vector DB Results with scrollbar
        ttk.Label(self.scrollable_frame, text="Vector DB Search Results:").grid(row=12, column=0, sticky="w", padx=10, pady=5)
        db_results_frame = ttk.Frame(self.scrollable_frame)
        db_results_frame.grid(row=13, column=0, sticky="nsew", padx=10, pady=5)
        db_results_scrollbar = ttk.Scrollbar(db_results_frame)
        db_results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.db_results = tk.Text(db_results_frame, height=10, wrap="word", yscrollcommand=db_results_scrollbar.set)
        self.db_results.pack(fill=tk.BOTH, expand=True)
        db_results_scrollbar.config(command=self.db_results.yview)

        # Log area with scrollbar and filter
        ttk.Label(self.scrollable_frame, text="Log (choose level):").grid(row=14, column=0, sticky="w", padx=10, pady=5)
        log_level_menu = ttk.Combobox(self.scrollable_frame, textvariable=self.log_level_filter,
                                      values=["ALL", "INFO", "DEBUG", "WARNING", "ERROR"], state="readonly")
        log_level_menu.grid(row=15, column=0, sticky="w", padx=10)
        log_frame = ttk.Frame(self.scrollable_frame)
        log_frame.grid(row=16, column=0, sticky="nsew", padx=10, pady=5)
        log_scrollbar = ttk.Scrollbar(log_frame)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_box = tk.Text(log_frame, height=10, wrap="word", state="disabled", yscrollcommand=log_scrollbar.set)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        log_scrollbar.config(command=self.log_box.yview)

        # Output file path display
        ttk.Label(self.scrollable_frame, text="Generated File Path:").grid(row=17, column=0, sticky="w", padx=10, pady=5)
        self.output_path_label = ttk.Entry(self.scrollable_frame, textvariable=self.generated_file_path, state="readonly", width=100)
        self.output_path_label.grid(row=18, column=0, sticky="we", padx=10, pady=5)

        # Configure grid weights for resizing
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(9, weight=1)   # BDD preview expand
        self.scrollable_frame.rowconfigure(13, weight=1)  # DB results expand
        self.scrollable_frame.rowconfigure(16, weight=1)  # Log box expand

    def toggle_custom_prompt(self, choice):
        if choice == "Custom":
            self.custom_prompt_entry.grid(row=5, column=1, sticky="w", padx=10)
        else:
            self.custom_prompt_entry.grid_forget()

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[
            ("Supported Files", "*.pdf *.docx *.png *.jpg *.py *.js *.java *.cpp *.cs *.ts *.go *.rb"),
            ("All files", "*.*")
        ])
        if filepath:
            self.selected_file.set(filepath)

    def run_threaded(self):
        self.bdd_preview.delete("1.0", tk.END)
        self.db_results.delete("1.0", tk.END)
        self.generated_file_path.set("")
        cancel_flag.clear()
        self.generate_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress["value"] = 0
        thread = threading.Thread(target=self.process_file, daemon=True)
        thread.start()

    def cancel_generation(self):
        cancel_flag.set()
        self.logger.warning("❌ Generation cancelled by user.")

    def process_file(self):
        path = self.selected_file.get()
        fmt = self.selected_format.get()
        domain = self.domain_choice.get()
        prompt = self.custom_prompt.get() if domain == "Custom" else domain

        if not os.path.exists(path):
            self.logger.error("⚠️ Invalid file path.")
            self.generate_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            return

        self.update_progress(10, "📄 Validating and generating preview...")

        try:
            # Preview-only generation
            bdd_text = process_file(path, fmt, prompt,
                                    progress_callback=self.update_progress,
                                    cancel_event=cancel_flag,
                                    preview_only=True)

            if cancel_flag.is_set():
                self.logger.warning("⚠️ Operation cancelled.")
                self.generate_button.config(state="normal")
                self.cancel_button.config(state="disabled")
                return

            self.bdd_preview.delete("1.0", tk.END)
            self.bdd_preview.insert(tk.END, bdd_text)
            self.update_progress(90, "✅ Preview generated.")

            # Full generation
            self.logger.info("💾 Saving BDD file...")
            output_path, _ = process_file(path, fmt, prompt,
                                          progress_callback=None,
                                          cancel_event=None,
                                          preview_only=False)

            self.generated_file_path.set(output_path)
            self.logger.info(f"✅ BDD saved to: {output_path}")
            self.update_progress(100, "✅ Done")

        except Exception as e:
            self.logger.error(f"❌ Error: {str(e)}")

        finally:
            self.generate_button.config(state="normal")
            self.cancel_button.config(state="disabled")

    def update_progress(self, pct, status):
        self.progress["value"] = pct
        self.logger.info(status)

    def search_by_tag(self, event=None):
        tag = self.tag_var.get()
        results = vector_store.search_by_tag(tag)
        self.db_results.delete("1.0", tk.END)
        if not results:
            self.db_results.insert(tk.END, "No entries found for this tag.")
            return
        for entry in results:
            self.db_results.insert(tk.END, f"Source: {entry['source_path']}\nDomain: {entry['domain_or_prompt']}\nTags: {entry.get('tags', [])}\nBDD Preview:\n{entry['output']}\n\n{'-'*40}\n")

    def copy_preview(self):
        text = self.bdd_preview.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No BDD scenario text to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "BDD preview copied to clipboard.")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#222222" if self.dark_mode else "SystemButtonFace"
        fg_color = "#eeeeee" if self.dark_mode else "black"

        # Apply colors to widgets
        widgets_to_color = [
            self.bdd_preview,
            self.db_results,
            self.log_box,
            self.custom_prompt_entry,
            self.output_path_label,
        ]
        for w in widgets_to_color:
            w.config(background=bg_color, foreground=fg_color, insertbackground=fg_color)

        # Change root bg
        self.root.config(bg=bg_color)
        self.scrollable_frame.config(style="TFrame")

    def setup_logger(self):
        self.logger = logging.getLogger("BDDLogger")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        file_handler = logging.FileHandler("app.log", encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        gui_handler = TkinterLogHandler(self.log_queue)
        gui_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(gui_handler)

    def poll_log_queue(self):
        try:
            while True:
                level, msg = self.log_queue.get_nowait()
                if self.log_level_filter.get() not in ["ALL", level]:
                    continue
                self.log_box.config(state='normal')
                self.log_box.insert(tk.END, msg + '\n', level)
                self.log_box.tag_config("INFO", foreground="black")
                self.log_box.tag_config("WARNING", foreground="orange")
                self.log_box.tag_config("ERROR", foreground="red")
                self.log_box.tag_config("DEBUG", foreground="gray")
                self.log_box.see(tk.END)
                self.log_box.config(state='disabled')
        except queue.Empty:
            pass
        self.root.after(100, self.poll_log_queue)

    def bind_shortcuts(self):
        self.root.bind("<Control-g>", lambda e: self.run_threaded())
        self.root.bind("<Control-G>", lambda e: self.run_threaded())
        self.root.bind("<Control-c>", lambda e: self.cancel_generation())
        self.root.bind("<Control-C>", lambda e: self.cancel_generation())
        # Save shortcut removed to avoid freeze

if __name__ == "__main__":
    root = tk.Tk()
    app = TestScenarioGUI(root)
    root.mainloop()
