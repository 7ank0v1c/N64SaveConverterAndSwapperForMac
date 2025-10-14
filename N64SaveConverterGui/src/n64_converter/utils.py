# utils.py

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
