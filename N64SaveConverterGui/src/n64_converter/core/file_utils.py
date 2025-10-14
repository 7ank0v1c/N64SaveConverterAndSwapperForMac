# file_utils.py

from datetime import datetime
import os

def new_filename(filename: str, extension: str, prefix: str = "Converted_") -> str:
    """
    Generate a new filename with a timestamp.

    Parameters:
        filename: Original file name.
        extension: Extension to append (with dot, e.g., '.sra').
        prefix: Optional prefix before timestamp.

    Returns:
        str: New filename, e.g., 'Converted_20251014-153245_MySave.sra'
    """
    base, _ = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}{timestamp}_{base}{extension}"
