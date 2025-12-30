import os

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".exe", ".dll",
    ".zip", ".tar", ".gz", ".pdf", ".mp4", ".mp3"
}

def is_binary_file(path):
    _, ext = os.path.splitext(path.lower())
    return ext in BINARY_EXTENSIONS
