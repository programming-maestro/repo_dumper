import os

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp",
    ".ico", ".mp4", ".mp3", ".zip", ".exe", ".pdf"
}

MAX_TEXT_FILE_SIZE = 1 * 1024 * 1024


def is_binary_file(path):
    return os.path.splitext(path.lower())[1] in BINARY_EXTENSIONS


def is_large_file(path):
    try:
        return os.path.getsize(path) > MAX_TEXT_FILE_SIZE
    except OSError:
        return True


def looks_binary_by_content(path):
    try:
        with open(path, "rb") as f:
            return b"\0" in f.read(1024)
    except Exception:
        return True
