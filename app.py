import tkinter as tk
from ui.main_window import RepoDumperApp

def main():
    root = tk.Tk()
    RepoDumperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
