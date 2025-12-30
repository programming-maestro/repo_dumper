import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from repo_scanner import scan_repository
from repo_writer import write_output_file
import threading


class RepoDumperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Repository Dumper")
        self.root.geometry("720x360")
        self.root.minsize(720, 360)

        self.repo_path = tk.StringVar()
        self.output_file = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")

        self.build_ui()

    def build_ui(self):
        # Main container
        container = ttk.Frame(self.root, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # ---- Title ----
        title = ttk.Label(
            container,
            text="Git Repository Dump Tool",
            font=("Segoe UI", 14, "bold")
        )
        title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))

        # ---- Repo Path ----
        ttk.Label(container, text="Repository Folder").grid(
            row=1, column=0, sticky="w", pady=5
        )

        repo_entry = ttk.Entry(
            container, textvariable=self.repo_path
        )
        repo_entry.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Button(
            container, text="Browse…", command=self.browse_repo
        ).grid(row=2, column=2, padx=(10, 0))

        # ---- Output File ----
        ttk.Label(container, text="Output File").grid(
            row=3, column=0, sticky="w", pady=(15, 5)
        )

        out_entry = ttk.Entry(
            container, textvariable=self.output_file
        )
        out_entry.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Button(
            container, text="Save As…", command=self.browse_output
        ).grid(row=4, column=2, padx=(10, 0))

        # ---- Action Button ----
        self.generate_btn = ttk.Button(
            container,
            text="Generate Repository Dump",
            command=self.start_generate
        )
        self.generate_btn.grid(
            row=5, column=0, columnspan=3, pady=(25, 10), sticky="ew"
        )

        # ---- Status Bar ----
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_text,
            relief="sunken",
            anchor="w",
            padding=8
        )
        status_bar.grid(row=1, column=0, sticky="ew")

        # Grid behavior
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

    # ---------------- Actions ----------------

    def browse_repo(self):
        path = filedialog.askdirectory()
        if path:
            self.repo_path.set(path)

    def browse_output(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file:
            self.output_file.set(file)

    def start_generate(self):
        if not self.repo_path.get() or not self.output_file.get():
            messagebox.showerror(
                "Missing Information",
                "Please select both repository folder and output file."
            )
            return

        self.generate_btn.config(state="disabled")
        self.status_text.set("Processing repository…")

        thread = threading.Thread(target=self.generate)
        thread.start()

    def generate(self):
        try:
            structure, contents = scan_repository(self.repo_path.get())
            write_output_file(self.output_file.get(), structure, contents)

            self.root.after(0, self.on_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_error(e))

    def on_success(self):
        self.generate_btn.config(state="normal")
        self.status_text.set("Completed successfully")
        messagebox.showinfo(
            "Success",
            "Repository dump created successfully."
        )

    def on_error(self, error):
        self.generate_btn.config(state="normal")
        self.status_text.set("Error occurred")
        messagebox.showerror("Error", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    RepoDumperGUI(root)
    root.mainloop()
