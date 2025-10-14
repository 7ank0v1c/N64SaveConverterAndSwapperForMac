# utils.py
import os
from tkinter import messagebox
from .constants import *

# Automatic file type detection
def detect_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == EEP_EXT:
        return EEP_LABEL
    elif ext == SRA_EXT:
        return SRA_LABEL
    elif ext == FLA_EXT:
        return FLA_LABEL
    elif ext == MPK_EXT:
        return MPK_LABEL
    elif ext == SRM_EXT:
        return SRM_LABEL
    else:
        return None

def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        messagebox.showerror("Error", f"Could not read file: {path}")
        return None

def write_bytes(data, path):
    try:
        with open(path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        messagebox.showerror("Error", f"Could not write file: {path}")
        return False

def resize_bytes(data, new_size, offset=0):
    """
    Resize data to new_size bytes.
    Positive offset: copy data starting at offset in new array.
    Negative offset: trim data from the start.
    """
    if offset < 0:
        data = data[abs(offset):]
        offset = 0

    result = bytearray(new_size)
    for i in range(len(data)):
        dest_index = i + offset
        if 0 <= dest_index < new_size:
            result[dest_index] = data[i]
    return bytes(result)
