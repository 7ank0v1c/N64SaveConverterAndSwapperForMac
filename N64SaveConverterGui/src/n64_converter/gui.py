# gui.py
import os
import platform
import subprocess
from datetime import datetime
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# --- Constants, settings, labels, lists, conversion_table, helper functions ---
# (Paste all your constants, conversion_table, detect_file_type, read_bytes, write_bytes,
# resize_bytes, byteswap, TermColors, determine_swap_size, new_filename functions here)
# Everything exactly as in your snippet above

def launch_gui():
    # --- GUI Setup ---
    root = Tk()
    root.title("N64 Save File Converter")
    root.geometry("730x380")
    root.resizable(False, False)
    root.grid_columnconfigure(0, minsize=180)

# Load N64 logo dynamically
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # location of gui.py
    resources_dir = os.path.join(base_dir, "resources")
    logo_path = os.path.join(resources_dir, "n64_logo.png")
    logo_img = PhotoImage(file=logo_path)
    root.iconphoto(True, logo_img)  # sets window and dock icon
except Exception:
    logo_img = None

    # --- Variables ---
    input_path = StringVar()
    source_type_var = StringVar()
    source_var = StringVar()
    target_var = StringVar()
    target_type_var = StringVar()
    trim_pad_var = BooleanVar()
    byteswap_var = StringVar(value="None")

    # --- GUI Components ---
    # (Paste all your Labels, Entry, Buttons, Comboboxes, Checkbuttons, log frame, log_box,
    # log tags, update_target_type_menu(), update_byteswap_menu(), toggle_log_window(), etc.)
    # Everything exactly as in your snippet above

    # --- Logging function ---
    # (Paste your log() function here)

    # --- Conversion function ---
    # (Paste your convert_save() function here)

    # --- Apply Theme ---
    # (Paste apply_theme(), widgets dict, poll_dark_mode() functions here)

    # --- Initialize ---
    update_byteswap_menu()
    update_target_type_menu()
    poll_dark_mode()
    root.mainloop()