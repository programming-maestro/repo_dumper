import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, PhotoImage
import threading

from core.scanner import scan_repository
from core.writer import write_output_file


class RepoDumperApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Repo Dumper")
        self.root.geometry("820x460")
        self.root.minsize(820, 460)

        self._load_icon()
        self._init_vars()
        self._configure_style()
        self._build_layout()

    # ---------- Setup ----------
    @staticmethod
    def resource_path(relative_path):
        """
        Get absolute path to resource, works for dev and PyInstaller
        """
        try:
            base_path = sys._MEIPASS  # PyInstaller temp folder
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def _load_icon(self):
        try:
            icon_path = RepoDumperApp.resource_path(
                os.path.join("assets", "repo_dumper.ico")
            )
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

    def _init_vars(self):
        self.repo_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.status = tk.StringVar(value="Ready")
        self.progress = tk.IntVar(value=0)

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Card.TFrame",
            background="#1e1e1e"
        )
        style.configure(
            "Title.TLabel",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 16, "bold")
        )
        style.configure(
            "Text.TLabel",
            background="#1e1e1e",
            foreground="#cfcfcf",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

    # ---------- Layout ----------

    def _build_layout(self):
        root = self.root
        root.configure(bg="#121212")

        container = ttk.Frame(root, style="Card.TFrame", padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Git Repository Dumper",
            style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 6))

        ttk.Label(
            container,
            text="Export complete repository structure and code into a single text file",
            style="Text.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        self._build_path_section(container)
        self._build_action_section(container)
        self._build_status_bar(container)

    def _build_path_section(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=10)

        # Repo
        ttk.Label(frame, text="Repository Folder", style="Text.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Entry(frame, textvariable=self.repo_path).grid(
            row=1, column=0, sticky="ew", padx=(0, 10)
        )
        ttk.Button(frame, text="Browse", command=self._browse_repo).grid(
            row=1, column=1
        )

        # Output
        ttk.Label(frame, text="Output File", style="Text.TLabel").grid(
            row=2, column=0, sticky="w", pady=(12, 0)
        )
        ttk.Entry(frame, textvariable=self.output_path).grid(
            row=3, column=0, sticky="ew", padx=(0, 10)
        )
        ttk.Button(frame, text="Save As", command=self._browse_output).grid(
            row=3, column=1
        )

        frame.columnconfigure(0, weight=1)

    def _build_action_section(self, parent):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=25)

        self.generate_btn = ttk.Button(
            frame,
            text="Generate Repository Dump",
            style="Primary.TButton",
            command=self._start
        )
        self.generate_btn.pack(fill="x")

        self.progress_bar = ttk.Progressbar(
            frame,
            variable=self.progress,
            maximum=100
        )
        self.progress_bar.pack(fill="x", pady=10)

    def _build_status_bar(self, parent):
        ttk.Label(
            parent,
            textvariable=self.status,
            style="Text.TLabel"
        ).pack(anchor="w", pady=(10, 0))

    # ---------- Actions ----------

    def _browse_repo(self):
        path = filedialog.askdirectory()
        if path:
            self.repo_path.set(path)

    def _browse_output(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if path:
            self.output_path.set(path)

    def _start(self):
        if not self.repo_path.get() or not self.output_path.get():
            messagebox.showerror("Error", "Select repository and output file")
            return

        self.generate_btn.config(state="disabled")
        self.status.set("Scanning repository...")
        self.progress.set(10)

        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        try:
            structure, contents, stats = scan_repository(self.repo_path.get())
            self.progress.set(70)

            write_output_file(
                self.output_path.get(),
                structure,
                contents,
                stats
            )

            self.root.after(0, self._success)
        except Exception as e:
            self.root.after(0, lambda: self._error(e))

    def _success(self):
        self.progress.set(100)
        self.status.set("Completed successfully")
        self.generate_btn.config(state="normal")
        messagebox.showinfo("Success", "Repository dump created!")

    def _error(self, error):
        self.progress.set(0)
        self.status.set("Failed")
        self.generate_btn.config(state="normal")
        messagebox.showerror("Error", str(error))

