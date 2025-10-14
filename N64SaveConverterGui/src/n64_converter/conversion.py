# conversion.py
import os
from datetime import datetime
from constants import *
from io_utils import read_bytes, write_bytes, resize_bytes
from swap_utils import byteswap, determine_swap_size

# Conversion table now includes Native
conversion_table = {
    # WII → RA/PJ64/NATIVE
    f"{WII_LABEL}-{EEP_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_EEP, SIZE_SRM, 0, False, SRM_EXT),
    f"{WII_LABEL}-{EEP_LABEL}-{NATIVE_LABEL}-{EEP_LABEL}": (SIZE_EEP, SIZE_EEP, 0, False, EEP_EXT),

    f"{WII_LABEL}-{SRA_LABEL}-{PJ64_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, True, SRA_EXT),
    f"{WII_LABEL}-{SRA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_SRA, SIZE_SRM, SIZE_SRA_SRM_OFFSET, True, SRM_EXT),
    f"{WII_LABEL}-{SRA_LABEL}-{NATIVE_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, False, SRA_EXT),

    f"{WII_LABEL}-{FLA_LABEL}-{PJ64_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, True, FLA_EXT),
    f"{WII_LABEL}-{FLA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_FLA, SIZE_SRM, SIZE_FLA_SRM_OFFSET, True, SRM_EXT),
    f"{WII_LABEL}-{FLA_LABEL}-{NATIVE_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, False, FLA_EXT),

    f"{WII_LABEL}-{MPK_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_MPK, SIZE_SRM, SIZE_MPK_SRM_OFFSET, False, SRM_EXT),
    f"{WII_LABEL}-{MPK_LABEL}-{NATIVE_LABEL}-{MPK_LABEL}": (SIZE_MPK, SIZE_MPK, 0, False, MPK_EXT),

    # PJ64 → RA/WII/NATIVE
    f"{PJ64_LABEL}-{EEP_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_EEP, SIZE_SRM, 0, False, SRM_EXT),
    f"{PJ64_LABEL}-{EEP_LABEL}-{NATIVE_LABEL}-{EEP_LABEL}": (SIZE_EEP, SIZE_EEP, 0, False, EEP_EXT),

    f"{PJ64_LABEL}-{SRA_LABEL}-{WII_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, True, SRA_EXT),
    f"{PJ64_LABEL}-{SRA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_SRA, SIZE_SRM, SIZE_SRA_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{SRA_LABEL}-{NATIVE_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, False, SRA_EXT),

    f"{PJ64_LABEL}-{FLA_LABEL}-{WII_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, True, FLA_EXT),
    f"{PJ64_LABEL}-{FLA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_FLA, SIZE_SRM, SIZE_FLA_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{FLA_LABEL}-{NATIVE_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, False, FLA_EXT),

    f"{PJ64_LABEL}-{MPK_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_MPK, SIZE_SRM, SIZE_MPK_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{MPK_LABEL}-{NATIVE_LABEL}-{MPK_LABEL}": (SIZE_MPK, SIZE_MPK, 0, False, MPK_EXT),

    # RA → PJ64/WII/NATIVE
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{EEP_LABEL}": (SIZE_SRM, SIZE_EEP, 0, False, EEP_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{SRA_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, True, SRA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{FLA_LABEL}": (SIZE_SRM, SIZE_FLA, -SIZE_FLA_SRM_OFFSET, True, FLA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{MPK_LABEL}": (SIZE_SRM, SIZE_MPK, -SIZE_MPK_SRM_OFFSET, False, MPK_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{NATIVE_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, True, SRA_EXT),  # generic example

    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{EEP_LABEL}": (SIZE_SRM, SIZE_EEP, 0, False, EEP_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{SRA_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, False, SRA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{FLA_LABEL}": (SIZE_SRM, SIZE_FLA, -SIZE_FLA_SRM_OFFSET, False, FLA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{MPK_LABEL}": (SIZE_SRM, SIZE_MPK, -SIZE_MPK_SRM_OFFSET, False, MPK_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{NATIVE_LABEL}-{SRA_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, False, SRA_EXT),

    # NATIVE → Anything else (raw dump, no offset)
    f"{NATIVE_LABEL}-{EEP_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_EEP, SIZE_SRM, 0, False, SRM_EXT),
    f"{NATIVE_LABEL}-{SRA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_SRA, SIZE_SRM, SIZE_SRA_SRM_OFFSET, True, SRM_EXT),
    f"{NATIVE_LABEL}-{FLA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_FLA, SIZE_SRM, SIZE_FLA_SRM_OFFSET, True, SRM_EXT),
    f"{NATIVE_LABEL}-{MPK_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_MPK, SIZE_SRM, SIZE_MPK_SRM_OFFSET, False, SRM_EXT),
    f"{NATIVE_LABEL}-{EEP_LABEL}-{PJ64_LABEL}-{EEP_LABEL}": (SIZE_EEP, SIZE_EEP, 0, False, EEP_EXT),
    f"{NATIVE_LABEL}-{SRA_LABEL}-{PJ64_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, True, SRA_EXT),
    f"{NATIVE_LABEL}-{FLA_LABEL}-{PJ64_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, True, FLA_EXT),
    f"{NATIVE_LABEL}-{MPK_LABEL}-{PJ64_LABEL}-{MPK_LABEL}": (SIZE_MPK, SIZE_MPK, 0, False, MPK_EXT),
}

# --- File type detection ---
def detect_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    mapping = {
        EEP_EXT: EEP_LABEL,
        SRA_EXT: SRA_LABEL,
        FLA_EXT: FLA_LABEL,
        MPK_EXT: MPK_LABEL,
        SRM_EXT: SRM_LABEL
    }
    return mapping.get(ext, None)

# --- Generate a new filename ---
def new_filename(orig_path, extension):
    base, _ = os.path.splitext(os.path.basename(orig_path))
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}_{base}{extension}"

# --- Main conversion function ---
def perform_conversion(input_path, src="", src_type="", tgt="", tgt_type="", swap_option="Default", pad_trim=True):
    """
    Converts N64 save files between formats.
    Returns converted bytes, new filename, or raises Exception.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    # Auto-detect source type if not provided
    if not src_type:
        src_type = detect_file_type(input_path)
        if not src_type:
            raise ValueError("Unable to detect source file type.")

    # Default target type if not provided
    if not tgt_type:
        tgt_type = src_type

    # Build conversion key
    key = f"{src}-{src_type}-{tgt}-{tgt_type}"

    # Read file
    data = read_bytes(input_path)
    if data is None:
        raise IOError("Failed to read input file.")

    # Lookup conversion table
    conv = conversion_table.get(key)
    if conv:
        src_size, tgt_size, offset, swap_required, extension = conv
    else:
        # Default to raw copy
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(input_path)[1]

    # Handle Native target
    if tgt == NATIVE_LABEL:
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(input_path)[1]

    # Apply resize/pad/trim
    if pad_trim:
        data = resize_bytes(data, tgt_size, offset)

    # Determine swap size
    swap_size = determine_swap_size(swap_required_from_table=swap_required, user_choice=swap_option)
    if swap_size > 1:
        data = byteswap(data, swap_size)

    # New filename
    new_name = new_filename(input_path, extension)

    return data, new_name