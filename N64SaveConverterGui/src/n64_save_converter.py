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

SIZE_SRA_SRM_OFFSET = 133120
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
target_list = [PJ64_LABEL, RA_LABEL, WII_LABEL]

# Conversion table
conversion_table = {
    f"{WII_LABEL}-{EEP_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_EEP, SIZE_SRM, 0, False, SRM_EXT),
    f"{WII_LABEL}-{SRA_LABEL}-{PJ64_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, True, SRA_EXT),
    f"{WII_LABEL}-{SRA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_SRA, SIZE_SRM, SIZE_SRA_SRM_OFFSET, True, SRM_EXT),
    f"{WII_LABEL}-{FLA_LABEL}-{PJ64_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, True, FLA_EXT),
    f"{WII_LABEL}-{FLA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_FLA, SIZE_SRM, SIZE_FLA_SRM_OFFSET, True, SRM_EXT),
    f"{WII_LABEL}-{MPK_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_MPK, SIZE_SRM, SIZE_MPK_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{EEP_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_EEP, SIZE_SRM, 0, False, SRM_EXT),
    f"{PJ64_LABEL}-{SRA_LABEL}-{WII_LABEL}-{SRA_LABEL}": (SIZE_SRA, SIZE_SRA, 0, True, SRA_EXT),
    f"{PJ64_LABEL}-{SRA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_SRA, SIZE_SRM, SIZE_SRA_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{FLA_LABEL}-{WII_LABEL}-{FLA_LABEL}": (SIZE_FLA, SIZE_FLA, 0, True, FLA_EXT),
    f"{PJ64_LABEL}-{FLA_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_FLA, SIZE_SRM, SIZE_FLA_SRM_OFFSET, False, SRM_EXT),
    f"{PJ64_LABEL}-{MPK_LABEL}-{RA_LABEL}-{SRM_LABEL}": (SIZE_MPK, SIZE_SRM, SIZE_MPK_SRM_OFFSET, False, SRM_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{EEP_LABEL}": (SIZE_SRM, SIZE_EEP, 0, False, EEP_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{SRA_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, True, SRA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{FLA_LABEL}": (SIZE_SRM, SIZE_FLA, -SIZE_FLA_SRM_OFFSET, True, FLA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{WII_LABEL}-{MPK_LABEL}": (SIZE_SRM, SIZE_MPK, -SIZE_MPK_SRM_OFFSET, False, MPK_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{EEP_LABEL}": (SIZE_SRM, SIZE_EEP, 0, False, EEP_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{SRA_LABEL}": (SIZE_SRM, SIZE_SRA, -SIZE_SRA_SRM_OFFSET, False, SRA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{FLA_LABEL}": (SIZE_SRM, SIZE_FLA, -SIZE_FLA_SRM_OFFSET, False, FLA_EXT),
    f"{RA_LABEL}-{SRM_LABEL}-{PJ64_LABEL}-{MPK_LABEL}": (SIZE_SRM, SIZE_MPK, -SIZE_MPK_SRM_OFFSET, False, MPK_EXT),
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
    result = bytearray(new_size)
    for i in range(new_size):
        if 0 <= i - offset < len(data):
            result[i] = data[i - offset]
    return bytes(result)

def byteswap(data, swap_size):
    if swap_size <= 1:
        return data
    swapped = bytearray(len(data))
    for i in range(0, len(data), swap_size):
        chunk = data[i:i+swap_size]
        swapped[i:i+len(chunk)] = chunk[::-1]
    return bytes(swapped)

def new_filename(filename, extension):
    base, ext = os.path.splitext(filename)
    if ext == extension:
        return base + "#" + extension
    return base + extension

# GUI setup
root = Tk()
root.title("N64 Save File Converter")
root.geometry("700x300")
root.resizable(False, False)

# Variables
input_path = StringVar()
source_var = StringVar()
source_type_var = StringVar()
target_var = StringVar()
target_type_var = StringVar()
trim_pad_var = BooleanVar()
byteswap_var = StringVar(value="None")

# GUI Components
Label(root, text="Select N64 Save File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=10, pady=5)
Button(root, text="Browse", command=lambda: input_path.set(filedialog.askopenfilename(filetypes=[("N64 Saves", "*.eep *.sra *.fla *.mpk *.srm")])))\
    .grid(row=0, column=2, padx=10, pady=5)

# Source
Label(root, text="Save File Source:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
source_menu = ttk.Combobox(root, textvariable=source_var, values=source_list, state="readonly")
source_menu.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Save File Source Type:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
source_type_menu = ttk.Combobox(root, textvariable=source_type_var, values=file_types, state="readonly")
source_type_menu.grid(row=2, column=1, padx=10, pady=5)

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

    # Get all matching types from the conversion table
    for key in conversion_table.keys():
        parts = key.split("-")
        if src == parts[0] and src_type == parts[1] and tgt == parts[2]:
            valid_output_types.add(parts[3])

    # Allow same-type conversion for SRA, FLA, MPK, SRM
    if src_type in ["SRAM (.sra)", "FlashRAM (.fla)", "Controller Pak (.mpk)", "Retroarch Save (.srm)"]:
        valid_output_types.add(src_type)

    # Update the target_type_menu values
    target_type_menu['values'] = sorted(list(valid_output_types))

    # Reset current selection if invalid
    if target_type_var.get() not in valid_output_types:
        target_type_var.set(sorted(list(valid_output_types))[0] if valid_output_types else "")

# Trace changes to update dynamically
source_var.trace_add("write", lambda *args: update_target_type_menu())
source_type_var.trace_add("write", lambda *args: update_target_type_menu())
target_var.trace_add("write", lambda *args: update_target_type_menu())

# Trim/Pad checkbox
Checkbutton(root, text="Pad/trim to standard file type size", variable=trim_pad_var).grid(row=5, column=1, sticky=W, padx=10, pady=5)

# Byte swap
Label(root, text="Byte Swap Size:").grid(row=6, column=0, sticky=W, padx=10, pady=5)
byteswap_menu = ttk.Combobox(root, textvariable=byteswap_var, values=["None", "2 bytes", "3 bytes", "4 bytes"], state="readonly")
byteswap_menu.grid(row=6, column=1, padx=10, pady=5)

def update_byteswap_menu(*args):
    # Show only for types that can benefit
    if source_type_var.get() in [SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL]:
        byteswap_menu.config(state="readonly")
    else:
        byteswap_menu.set("None")
        byteswap_menu.config(state="disabled")

source_type_var.trace_add("write", lambda *args: update_byteswap_menu())
target_type_var.trace_add("write", lambda *args: update_byteswap_menu())

# Convert button
def convert_save():
    path = input_path.get()
    if not path or not os.path.exists(path):
        messagebox.showerror("Error", "Please select a valid input file.")
        return

    data = read_bytes(path)
    if not data:
        return

    # Determine conversion
    src = source_var.get()
    src_type = source_type_var.get()
    tgt = target_var.get()
    tgt_type = target_type_var.get()
    key = f"{src}-{src_type}-{tgt}-{tgt_type}"

    # Determine conversion parameters
    if key in conversion_table:
        src_size, tgt_size, offset, swap_required, extension = conversion_table[key]
    else:
        # Default: allow same type conversion
        src_size = tgt_size = len(data)
        offset = 0
        swap_required = False
        extension = os.path.splitext(path)[1]

    # Apply trimming/padding
    if trim_pad_var.get():
        data = resize_bytes(data, tgt_size, offset)

    # Apply byte swapping if requested
    swap_map = {"None": 1, "2 bytes": 2, "3 bytes": 3, "4 bytes": 4}
    swap_size = swap_map.get(byteswap_var.get(), 1)
    if swap_size > 1:
        data = byteswap(data, swap_size)

    # Determine output filename
    out_path = filedialog.asksaveasfilename(
        initialfile=new_filename(os.path.basename(path), extension),
        defaultextension=extension,
        filetypes=[("N64 Save Files", f"*{extension}")]
    )
    if not out_path:
        return

    if write_bytes(data, out_path):
        messagebox.showinfo("Success", f"File converted and saved as:\n{out_path}")

Button(root, text="Convert", command=convert_save, width=20).grid(row=7, column=1, padx=10, pady=20)

root.mainloop()
