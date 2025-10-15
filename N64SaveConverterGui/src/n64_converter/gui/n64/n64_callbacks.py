# gui/n64/n64_callbacks.py

import os
from tkinter import messagebox, filedialog
from core.file_utils import read_bytes, write_bytes, resize_bytes, new_filename
from core.swap_utils import byteswap, determine_swap_size
from core.logger import log
from conversions.n64_conversion_table import conversion_table
from core.constants.n64_constants import *

def convert_save_n64(input_path_var, source_var, source_type_var,
                     target_var, target_type_var, byteswap_var,
                     trim_pad_var, log_box):
    """
    Performs N64 save file conversion using conversion table and rules.
    """
    path = input_path_var.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid input file.")
        return

    src = source_var.get()
    src_type = source_type_var.get()
    tgt = target_var.get()
    tgt_type = target_type_var.get()
    key = f"{src}-{src_type}-{tgt}-{tgt_type}"

    log(f"Starting conversion for: {path}", log_box, key, level="INFO")

    data = read_bytes(path)
    if not data:
        log("Error: Unable to read data from file.", log_box, key, level="ERROR")
        return

    log(f"Source: {src} ({src_type}) → Target: {tgt} ({tgt_type})", log_box, key, level="INFO")

    # --- Determine conversion from table ---
    tgt_size = len(data)
    offset = 0
    swap_required = False
    extension = os.path.splitext(path)[1]

    conv = conversion_table.get(key)
    if conv:
        src_size, tgt_size, offset, swap_required, extension = conv
        log(f"Using conversion table entry: {key}", log_box, key, level="INFO")
    else:
        log("No matching conversion found; defaulting to raw copy.", log_box, key, level="WARN")

    # Handle Native target separately
    if tgt == NATIVE_LABEL:
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(path)[1]
        log("Target is Native — using direct copy settings.", log_box, key, level="INFO")

    # Additional SRM-specific offsets
    if src_type == SRA_LABEL and tgt_type == SRM_LABEL:
        tgt_size = SIZE_SRM
        offset = SIZE_SRA_SRM_OFFSET
        swap_required = True
        extension = SRM_EXT
    elif src_type == FLA_LABEL and tgt_type == SRM_LABEL:
        tgt_size = SIZE_SRM
        offset = SIZE_FLA_SRM_OFFSET
        swap_required = True
        extension = SRM_EXT
    elif src_type == MPK_LABEL and tgt_type == SRM_LABEL:
        tgt_size = SIZE_SRM
        offset = SIZE_MPK_SRM_OFFSET
        swap_required = False
        extension = SRM_EXT
    elif src_type == SRM_LABEL:
        if tgt_type == SRA_LABEL:
            tgt_size = SIZE_SRA
            offset = -SIZE_SRA_SRM_OFFSET
            swap_required = True
            extension = SRA_EXT
        elif tgt_type == FLA_LABEL:
            tgt_size = SIZE_FLA
            offset = -SIZE_FLA_SRM_OFFSET
            swap_required = True
            extension = FLA_EXT
        elif tgt_type == MPK_LABEL:
            tgt_size = SIZE_MPK
            offset = -SIZE_MPK_SRM_OFFSET
            swap_required = False
            extension = MPK_EXT
        elif tgt_type == EEP_LABEL:
            tgt_size = SIZE_EEP
            offset = 0
            swap_required = False
            extension = EEP_EXT
    elif src_type == EEP_LABEL and tgt_type == SRM_LABEL:
        tgt_size = SIZE_SRM
        offset = 0
        swap_required = False
        extension = SRM_EXT

    log(f"Resizing data to {tgt_size} bytes (offset {offset})", log_box, key)
    data = resize_bytes(data, tgt_size, offset)

    # Byte swap
    swap_size = determine_swap_size(swap_required_from_table=swap_required,
                                    user_choice=byteswap_var.get())
    if swap_size > 1:
        log(f"Applying {swap_size}-byte swap...", log_box, key)
        data = byteswap(data, swap_size)
    else:
        log("No byte swap applied.", log_box, key)

    # Determine output extension
    ext_map = {EEP_LABEL: EEP_EXT, SRA_LABEL: SRA_EXT, FLA_LABEL: FLA_EXT,
               MPK_LABEL: MPK_EXT, SRM_LABEL: SRM_EXT}
    out_ext = ext_map.get(tgt_type, extension)
    new_name = new_filename(os.path.basename(path), out_ext)

    # Save file
    out_path = filedialog.asksaveasfilename(
        initialfile=new_name,
        defaultextension=out_ext,
        filetypes=[("N64 Save Files", f"*{out_ext}")]
    )
    if not out_path:
        log("Save operation cancelled by user.", log_box, key)
        return

    if write_bytes(data, out_path):
        log(f"File written successfully → {out_path}", log_box, key)
        messagebox.showinfo("Success", f"File converted and saved as:\n{out_path}")
    else:
        log("Error writing file.", log_box, key)
