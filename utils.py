# utils.py
import os

# --- Explicit categories ---
IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".svg"
}

MEDIA_EXTENSIONS = {
    ".mp4", ".mp3", ".wav", ".avi", ".mov", ".mkv"
}

ARCHIVE_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".7z", ".rar"
}

EXECUTABLE_EXTENSIONS = {
    ".exe", ".dll", ".so", ".bin"
}

DOCUMENT_EXTENSIONS = {
    ".pdf", "xls", "xlsx", "doc", "docx", "ppt", "pptx"
}

BINARY_EXTENSIONS = (
    IMAGE_EXTENSIONS
    | MEDIA_EXTENSIONS
    | ARCHIVE_EXTENSIONS
    | EXECUTABLE_EXTENSIONS
    | DOCUMENT_EXTENSIONS
)

MAX_TEXT_FILE_SIZE = 1 * 1024 * 1024  # 1 MB


def is_binary_file(path):
    _, ext = os.path.splitext(path.lower())
    return ext in BINARY_EXTENSIONS


def is_large_file(path):
    try:
        return os.path.getsize(path) > MAX_TEXT_FILE_SIZE
    except OSError:
        return True


def looks_binary_by_content(path):
    """
    Byte-level binary sniffing.
    """
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        return b"\0" in chunk
    except Exception:
        return True
