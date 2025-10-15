import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# Import N64 Constants (core/n64_constants.py)
from systems.n64.n64_constants import (
    EEP_EXT, SRA_EXT, FLA_EXT, MPK_EXT, SRM_EXT,
    SIZE_EEP, SIZE_SRA, SIZE_FLA, SIZE_MPK, SIZE_SRM,
    SIZE_SRA_SRM_OFFSET, SIZE_FLA_SRM_OFFSET, SIZE_MPK_SRM_OFFSET,
    EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL,
    NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL,
    FILE_TYPES, SOURCE_LIST, TARGET_LIST
)

# Automatic file type detection + Read, Write, Resize Bytes (core/file_utils.py)
from core.file_utils import detect_file_type, read_bytes, write_bytes, resize_bytes, new_filename

# N64 Conversion table (conversions/n64_conversion_table.py)
from systems.n64.n64_conversion_table import conversion_table

# Define Byteswap (core/swap_utils.py)
from core.swap_utils import byteswap, determine_swap_size

# Load logger module (core/logger.py)
from core.logger import log

# Terminal Colours + Gui Log (core/log_utils.py)
from core.log_utils import TermColors, gui_log

# Theme Utilities (core/theme_utils.py)
from core.theme_utils import *

# Gui Callbacks (gui/callbacks.py)
from gui import callbacks

from systems.n64.gui import n64_callbacks

# GUI setup
root = Tk()
root.title("N64 Save File Converter")
root.geometry("730x380")
root.resizable(False, False)
root.grid_columnconfigure(0, minsize=180)  # ensures column 1 widgets align horizontally

# --- Secondary GUI log window ---
log_window = None

# Load N64 logo and set as window/dock icon
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(base_dir, "resources")
    logo_path = os.path.join(resources_dir, "n64_logo.png")
    logo_img = PhotoImage(file=logo_path)
    root.iconphoto(True, logo_img)  # sets window and dock icon
except Exception:
    logo_img = None

logo_label = Label(
    root,
    image=logo_img if logo_img else None,
    text="N64 Logo" if not logo_img else "",
    compound="top"
)
logo_label.grid(row=7, column=2, padx=10, pady=10, sticky=E)

# Variables
input_path = StringVar()
source_type_var = StringVar()
source_var = StringVar()
target_var = StringVar()
target_type_var = StringVar()
trim_pad_var = BooleanVar()
byteswap_var = StringVar(value="None")

# GUI Components
Label(root, text="Select N64 Save File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
directory_entry = Entry(root, textvariable=input_path, width=45)
directory_entry.grid(row=0, column=1, padx=10, pady=5)

# Always scroll Entry view to the end when text changes or user edits
def scroll_to_end(*args):
    root.after_idle(lambda: directory_entry.xview_moveto(1))

input_path.trace_add("write", scroll_to_end)
directory_entry.bind("<KeyRelease>", lambda e: directory_entry.xview_moveto(1))
directory_entry.bind("<<Paste>>", lambda e: root.after_idle(lambda: directory_entry.xview_moveto(1)))

#Browse button, calls the generic helper:
Button(root, text="Browse", command=lambda: callbacks.browse_file(
    filetypes=[("N64 Saves", "*.eep *.sra *.fla *.mpk *.srm")],
    path_var=input_path,
    type_var=source_type_var
)).grid(row=0, column=2, padx=10, pady=5)

# --- INLINE LOG FRAME (right side, scrollable) ---
log_frame = Frame(root, bg="#111")
log_frame.grid(row=0, column=3, rowspan=9, sticky="nsew", padx=5, pady=5)
root.grid_columnconfigure(3, weight=1)

log_label = Label(log_frame, text="Conversion Log:", bg="#111", fg="#fff")
log_label.pack(anchor="w", padx=5, pady=(5,0))

# Wrap Text in a fixed-height subframe
log_text_frame = Frame(log_frame, height=200, bg="#111")  # fixed height in pixels
log_text_frame.pack(fill=BOTH, expand=False, padx=5, pady=5)

log_box = Text(log_text_frame, height=25, width=50, wrap="word", bg="#111", fg="#ddd")
log_box.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = Scrollbar(log_text_frame, command=log_box.yview)
scrollbar.pack(side=RIGHT, fill=Y)
log_box.config(yscrollcommand=scrollbar.set)

# GUI tags
log_box.tag_config("timestamp", foreground="#FFA500")  # orange
log_box.tag_config("level_info", foreground="#FFFFFF") # white
log_box.tag_config("level_conversion", foreground="#00FFFF") # cyan
log_box.tag_config("level_warn", foreground="#FFD700") # yellow
log_box.tag_config("level_error", foreground="#FF4500") # red
log_box.tag_config("level_success", foreground="#00FF00")  # bright green

# --- Toggle Function ---
log_visible = True  # log open by default
root.geometry("1000x380")  # wider to accommodate log on launch

def toggle_log_window():
    global log_visible
    if log_visible:
        log_frame.grid_remove()
        root.geometry("730x380")  # shrink main window
        log_visible = False
    else:
        log_frame.grid()
        root.geometry("1000x380")  # expand main window
        log_visible = True

# Toggle Button
Button(root, text="Show/Hide Log", command=toggle_log_window).grid(row=7, column=0, pady=15, padx=5)

# Source
Label(root, text="Save File Source Type:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
source_type_label = Label(root, textvariable=source_type_var, relief="flat", width=22, anchor=W)
source_type_label.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Save File Source:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
source_menu = ttk.Combobox(root, textvariable=source_var, values=SOURCE_LIST, state="readonly")
source_menu.grid(row=2, column=1, padx=10, pady=5)

# Target
Label(root, text="Save File Target:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
target_menu = ttk.Combobox(root, textvariable=target_var, values=TARGET_LIST, state="readonly")
target_menu.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Save File Target Type:").grid(row=4, column=0, sticky=W, padx=10, pady=5)

# Dynamic target type menu
target_type_menu = ttk.Combobox(root, textvariable=target_type_var, state="readonly")
target_type_menu.grid(row=4, column=1, padx=10, pady=5)

# Function to update target types based on source, source type, and target
def update_target_type_menu(*args):
    src = source_var.get()
    src_type = source_type_var.get()
    tgt = target_var.get()
    valid_output_types = set()

    # --- SRM as source ---
    if src_type == SRM_LABEL:
        valid_output_types.update([EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL])

    # --- EEP/SRA/FLA/MPK as source ---
    elif src_type in [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL]:
        if tgt in [PJ64_LABEL, WII_LABEL, NATIVE_LABEL]:
            valid_output_types.add(src_type)
        elif tgt == RA_LABEL:
            valid_output_types.add(SRM_LABEL)

    # --- Native as source ---
    elif src == NATIVE_LABEL:
        # For Native source, target type is same as src_type
        if src_type in [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL]:
            valid_output_types.add(src_type)
        elif src_type == SRM_LABEL:
            valid_output_types.add(SRM_LABEL)

    # Sort and set menu
    valid_output_types = sorted(valid_output_types)
    target_type_menu['values'] = valid_output_types

    # Default to first option if current selection is invalid
    if target_type_var.get() not in valid_output_types:
        target_type_var.set(valid_output_types[0] if valid_output_types else "")

# Update the traces
source_var.trace_add("write", update_target_type_menu)
source_type_var.trace_add("write", update_target_type_menu)
target_var.trace_add("write", update_target_type_menu)

Checkbutton(
    root,
    text="Pad/trim to standard file type size",
    variable=trim_pad_var,
    anchor="e",
    justify="center"
).grid(row=5, column=1, sticky=W+E, padx=100, pady=5)

# Byte swap
Label(root, text="Force Byte Swap:").grid(row=6, column=0, sticky=W, padx=10, pady=5)
byteswap_menu = ttk.Combobox(
    root,
    textvariable=byteswap_var,
    values=["Default", "2 bytes", "4 bytes"],
    state="readonly"
)
byteswap_menu.grid(row=6, column=1, padx=10, pady=5)

def update_byteswap_menu(*args):
    src_type = source_type_var.get()
    tgt_type = target_type_var.get()
    # Allow byte-swapping only for formats where endianess matters
    if src_type in [SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL]:
        byteswap_menu.config(state="readonly")
        if byteswap_var.get() not in ["Default", "2 bytes", "4 bytes"]:
            byteswap_var.set("Default")
    else:
        byteswap_var.set("Default")
        byteswap_menu.config(state="disabled")

# Trace variable changes to refresh byte-swap dropdown automatically
source_type_var.trace_add("write", update_byteswap_menu)
target_type_var.trace_add("write", update_byteswap_menu)

# GUI tags
log_box.tag_config("timestamp", foreground="#FFA500")  # orange
log_box.tag_config("level_info", foreground="#FFFFFF") # white
log_box.tag_config("level_conversion", foreground="#00FFFF") # cyan
log_box.tag_config("level_warn", foreground="#FFD700") # yellow
log_box.tag_config("level_error", foreground="#FF4500") # red

# Convert button
Button(root, text="Convert", width=20, command=lambda: n64_callbacks.convert_save_n64(
    input_path=input_path,
    source_var=source_var,
    source_type_var=source_type_var,
    target_var=target_var,
    target_type_var=target_type_var,
    byteswap_var=byteswap_var,
    trim_pad_var=trim_pad_var,
    log_box=log_box
)).grid(row=7, column=1, pady=15)

update_byteswap_menu()
update_target_type_menu()

# Apply theme and start polling for system dark/light changes
apply_theme(root)       # automatically detects widgets
start_polling(root)     # keeps theme updated

root.mainloop()
