import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# Import N64 Constants (core/n64_constants.py)
from core.constants.n64_constants import (
    EEP_EXT, SRA_EXT, FLA_EXT, MPK_EXT, SRM_EXT,
    SIZE_EEP, SIZE_SRA, SIZE_FLA, SIZE_MPK, SIZE_SRM,
    EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL,
    NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL,
    FILE_TYPES, SOURCE_LIST, TARGET_LIST
)

# Automatic file type detection + Read, Write, Resize Bytes (core/file_utils.py)
from core.file_utils import detect_file_type, read_bytes, write_bytes, resize_bytes, new_filename

# N64 Conversion table (conversions/n64_conversion_table.py)
from conversions.n64_conversion_table import conversion_table

# Define Byteswap (core/swap_utils.py)
from core.swap_utils import byteswap, determine_swap_size

# Terminal Colours + Gui Log (core/log_utils.py)
from core.log_utils import TermColors, gui_log

# Theme Utilities (core/theme_utils.py)
from core.theme_utils import *

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
def browse_file():
    path = filedialog.askopenfilename(filetypes=[("N64 Saves", "*.eep *.sra *.fla *.mpk *.srm")])
    if path:
        input_path.set(path)
        # Detect type
        selected_type = detect_file_type(path)
        if selected_type in file_types:  # ensure it’s valid
            source_type_var.set(selected_type)
        else:
            source_type_var.set("")  # fallback if detection fails

Label(root, text="Select N64 Save File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
directory_entry = Entry(root, textvariable=input_path, width=45)
directory_entry.grid(row=0, column=1, padx=10, pady=5)

# Always scroll Entry view to the end when text changes or user edits
def scroll_to_end(*args):
    root.after_idle(lambda: directory_entry.xview_moveto(1))

input_path.trace_add("write", scroll_to_end)
directory_entry.bind("<KeyRelease>", lambda e: directory_entry.xview_moveto(1))
directory_entry.bind("<<Paste>>", lambda e: root.after_idle(lambda: directory_entry.xview_moveto(1)))

# Browse Button
Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)

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
source_menu = ttk.Combobox(root, textvariable=source_var, values=source_list, state="readonly")
source_menu.grid(row=2, column=1, padx=10, pady=5)

# Target
Label(root, text="Save File Target:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
target_menu = ttk.Combobox(root, textvariable=target_var, values=target_list, state="readonly")
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

# --- Updated Log Function ---
from datetime import datetime
def log(message, key=None, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Determine terminal color ---
    term_color_map = {
        "INFO": "\033[37m",   # white
        "WARN": "\033[33m",   # yellow
        "ERROR": "\033[31m",  # red
    }
    conversion_color = "\033[36m"  # cyan
    timestamp_color = "\033[38;5;214m"  # orange
    reset = "\033[0m"

    # --- Terminal output ---
    if "Using conversion table entry" in message:
        print(f"{timestamp_color}[{timestamp}]{reset} {conversion_color}{message}{reset}")
    else:
        print(f"{timestamp_color}[{timestamp}]{reset} {term_color_map.get(level, '\033[37m')}{message}{reset}")

    # --- GUI log ---
    tag = "level_info"
    if level == "WARN":
        tag = "level_warn"
    elif level == "ERROR":
        tag = "level_error"
    elif "Using conversion table entry" in message:
        tag = "level_conversion"

    # --- Main log box ---
    log_box.insert(END, f"[{timestamp}]", "timestamp")
    if key and "Using conversion table entry" not in message:
        log_box.insert(END, f" [{key}]")
    log_box.insert(END, f" {message}\n", tag)
    log_box.see(END)
    log_box.update_idletasks()  # <-- Force real-time update

    # --- Log to file ---
    with open("conversion_log.txt", "a") as f:
        f.write(f"[{timestamp}]" + (f" [{key}]" if key and "Using conversion table entry" not in message else "") + f" {message}\n")

# GUI tags
log_box.tag_config("timestamp", foreground="#FFA500")  # orange
log_box.tag_config("level_info", foreground="#FFFFFF") # white
log_box.tag_config("level_conversion", foreground="#00FFFF") # cyan
log_box.tag_config("level_warn", foreground="#FFD700") # yellow
log_box.tag_config("level_error", foreground="#FF4500") # red

# Update secondary GUI log if open
if log_window and log_window.winfo_exists():
    log_window.log_text.config(state="normal")
    log_window.log_text.insert(END, f"[{timestamp}]" + (f" [{key}]" if key else "") + f" {message}\n")
    log_window.log_text.see(END)
    log_window.log_text.config(state="disabled")

# Convert Function
def convert_save():
    path = input_path.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid input file.")
        return

    # Get source/target info
    src = source_var.get()
    src_type = source_type_var.get()
    tgt = target_var.get()
    tgt_type = target_type_var.get()

    # --- DEFINE KEY FIRST ---
    key = f"{src}-{src_type}-{tgt}-{tgt_type}"

    # Now safe to log using key
    log(f"Starting conversion for: {path}", key, level="INFO")

    data = read_bytes(path)
    if not data:
        log("Error: Unable to read data from file.", key, level="ERROR")
        return

    log(f"Source: {src} ({src_type}) → Target: {tgt} ({tgt_type})", key, level="INFO")

    # --- Continue with conversion logic ---
    tgt_size = len(data)
    offset = 0
    swap_required = False
    extension = os.path.splitext(path)[1]

    conv = conversion_table.get(key)
    if conv:
        src_size, tgt_size, offset, swap_required, extension = conv
        log(f"Using conversion table entry: {key}", key, level="INFO")
    else:
        log("No matching conversion found; defaulting to raw copy.", key, level="WARN")

    # Handle Native target separately
    if tgt == NATIVE_LABEL:
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(path)[1]
        log("Target is Native — using direct copy settings.", key, level="INFO")

    # Additional offsets for certain SRM conversions
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

    # Now safe to log
    log(f"Resizing data to {tgt_size} bytes (offset {offset})", key)
    data = resize_bytes(data, tgt_size, offset)

    # Determine swap size based on conversion table first, then force option
    swap_size = determine_swap_size(
        swap_required_from_table=swap_required,
        user_choice=byteswap_var.get()
    )

    if swap_size > 1:
        log(f"Applying {swap_size}-byte swap...", key)
        data = byteswap(data, swap_size)
    else:
        log("No byte swap applied.", key)

    # Determine output extension
    ext_map = {
        EEP_LABEL: EEP_EXT,
        SRA_LABEL: SRA_EXT,
        FLA_LABEL: FLA_EXT,
        MPK_LABEL: MPK_EXT,
        SRM_LABEL: SRM_EXT
    }
    out_ext = ext_map.get(tgt_type, extension)
    new_name = new_filename(os.path.basename(path), out_ext)

    # Save file
    out_path = filedialog.asksaveasfilename(
        initialfile=new_name,
        defaultextension=out_ext,
        filetypes=[("N64 Save Files", f"*{out_ext}")]
    )
    if not out_path:
        log("Save operation cancelled by user.", key)
        return

    if write_bytes(data, out_path):
        log(f"File written successfully → {out_path}", key)
        messagebox.showinfo("Success", f"File converted and saved as:\n{out_path}")
    else:
        log("Error writing file.", key)

# Convert button
Button(root, text="Convert", width=20, command=convert_save).grid(row=7, column=1, pady=15)

update_byteswap_menu()
update_target_type_menu()

# Apply theme and start polling for system dark/light changes
apply_theme(root)       # automatically detects widgets
start_polling(root)     # keeps theme updated

root.mainloop()
