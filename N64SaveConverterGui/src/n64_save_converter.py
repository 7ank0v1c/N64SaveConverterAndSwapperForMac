import os
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# Constants
EEP_EXT = ".eep"
SRA_EXT = ".sra"
FLA_EXT = ".fla"
MPK_EXT = ".mpk"
SRM_EXT = ".srm"

SIZE_EEP = 2048
SIZE_SRA = 32768
SIZE_FLA = 131072
SIZE_MPK = 131072
SIZE_SRM = 296960

SIZE_SRA_SRM_OFFSET = 133120  # SRA 32 KB will sit inside 296960-byte SRM
SIZE_FLA_SRM_OFFSET = SIZE_SRM - SIZE_FLA
SIZE_MPK_SRM_OFFSET = 2048

# Labels
EEP_LABEL = "EEPROM (.eep)"
SRA_LABEL = "SRAM (.sra)"
FLA_LABEL = "FlashRAM (.fla)"
MPK_LABEL = "Controller Pak (.mpk)"
SRM_LABEL = "Retroarch Save (.srm)"

NATIVE_LABEL = "Native / Cart Dump"
PJ64_LABEL = "Project64/Mupen64"
RA_LABEL = "Retroarch"
WII_LABEL = "Wii/WiiU/Everdrive64"

# File type lists
file_types = [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL]
source_list = [NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL]
target_list = [NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL]

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

# Helper functions
def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except:
        messagebox.showerror("Error", f"Could not read file: {path}")
        return None

def write_bytes(data, path):
    try:
        with open(path, "wb") as f:
            f.write(data)
        return True
    except:
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

def byteswap(data, swap_size):
    if swap_size <= 1:
        return data
    swapped = bytearray(len(data))
    for i in range(0, len(data), swap_size):
        chunk = data[i:i+swap_size]
        swapped[i:i+len(chunk)] = chunk[::-1]
    return bytes(swapped)

def determine_swap_size(src_type, tgt_type, user_choice, swap_required_from_table=False):
    """
    Returns swap size in bytes based on user selection and table flag.
    'Default' uses only the conversion table (swap_required_from_table).
    """
    if user_choice == "2 bytes":
        return 2
    elif user_choice == "4 bytes":
        return 4
    elif user_choice == "Default":
        return 2 if swap_required_from_table else 1
    return 1

def new_filename(filename, extension):
    base, _ = os.path.splitext(filename)
    return f"{base}{extension}"

# GUI setup
root = Tk()
root.title("N64 Save File Converter")
root.geometry("730x380")
root.resizable(False, False)
root.grid_columnconfigure(0, minsize=180)  # ensures column 1 widgets align horizontally

# Load N64 logo and set as window/dock icon
try:
    logo_path = os.path.join(os.path.dirname(__file__), "n64_logo.png")
    logo_img = PhotoImage(file=logo_path)
    root.iconphoto(True, logo_img)  # sets icon for window and taskbar/dock
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

Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)

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

    # Basic mode: show only "realistic" options
    if src_type == SRM_LABEL:
        # Allow SRM -> any supported save type (EEP, SRA, FLA, MPK)
        valid_output_types.update([EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL])
    elif tgt == PJ64_LABEL:
        if src_type in [SRA_LABEL, FLA_LABEL, MPK_LABEL, EEP_LABEL]:
            valid_output_types.add(src_type)
    elif tgt == RA_LABEL:
        valid_output_types.add(SRM_LABEL)
    elif tgt in [WII_LABEL, NATIVE_LABEL]:
        valid_output_types.add(src_type)

    valid_output_types = sorted(list(valid_output_types))
    target_type_menu['values'] = valid_output_types

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

# Convert Function
def convert_save():
    path = input_path.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid input file.")
        return

    data = read_bytes(path)
    if not data:
        return

    src = source_var.get()
    src_type = source_type_var.get()
    tgt = target_var.get()
    tgt_type = target_type_var.get()
    key = f"{src}-{src_type}-{tgt}-{tgt_type}"

    # Determine conversion parameters
    conv = conversion_table.get(key)
    if conv:
        src_size, tgt_size, offset, swap_required, extension = conv
    else:
        # fallback
        src_size = len(data)
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(path)[1]

    # Handle Native target separately
    if tgt == NATIVE_LABEL:
        tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(path)[1]

    # JS-style logic: determine offset and size based on type combos
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

    # Resize / pad / trim
    data = resize_bytes(data, tgt_size, offset)

    # Determine swap size using the new helper function
    swap_size = determine_swap_size(src_type, tgt_type, byteswap_var.get(), swap_required)
    if swap_size > 1:
        data = byteswap(data, swap_size)

    # Determine output extension
    ext_map = {
        EEP_LABEL: EEP_EXT,
        SRA_LABEL: SRA_EXT,
        FLA_LABEL: FLA_EXT,
        MPK_LABEL: MPK_EXT,
        SRM_LABEL: SRM_EXT
    }
    out_ext = ext_map.get(tgt_type, os.path.splitext(path)[1])

    # Save file
    out_path = filedialog.asksaveasfilename(
        initialfile=new_filename(os.path.basename(path), out_ext),
        defaultextension=out_ext,
        filetypes=[("N64 Save Files", f"*{out_ext}")]
    )
    if not out_path:
        return

    if write_bytes(data, out_path):
        messagebox.showinfo("Success", f"File converted and saved as:\n{out_path}")

# Convert button
Button(root, text="Convert", width=20, command=convert_save).grid(row=7, column=1, pady=15)

update_byteswap_menu()

update_target_type_menu()

root.mainloop()
