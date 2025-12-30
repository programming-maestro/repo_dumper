# Git Repository Dumper

A lightweight, GUI-based Python tool to **export a complete Git repository structure and source code** into a single, human-readable text file — while **respecting `.gitignore` rules** and excluding unwanted or sensitive files.

This tool is especially useful for:
- Sharing full repositories with LLMs
- Code reviews and audits
- Documentation and archival
- Offline analysis of project structure

---

## ✨ Features

- 📁 **Accurate repository tree generation**
- 🧠 **Git-aware ignore logic**
  - Honors `.gitignore` (including nested rules)
  - Hard-excludes `.git`, `.idea`, `.venv`, `__pycache__`
- 📄 **Source code extraction**
  - Includes full content of text files
  - Automatically skips binary files
- 🔒 **Safe by design**
  - `.gitignore` is used for logic only
  - `.gitignore` content is never dumped
- 🖥️ **Clean desktop GUI**
  - Built with Tkinter (`ttk`)
  - Status feedback and non-blocking execution
- ⚡ **Minimal dependencies**

---

## 📂 Project Structure

```text
repo_dumper/
├── repo_dumper_gui.py   # GUI application (entry point)
├── repo_scanner.py      # Repository traversal & ignore logic
├── repo_writer.py       # Output file formatting
├── utils.py             # Helper utilities
└── requirements.txt     # External dependencies
