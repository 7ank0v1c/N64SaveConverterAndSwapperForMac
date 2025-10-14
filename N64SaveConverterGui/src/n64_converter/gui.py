# gui.py
import os
import platform
import subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox

# --- Imports from other modules ---
from constants import *             # constants, labels, file types
from conversion import perform_conversion, detect_file_type  # conversion logic
from io_utils import read_bytes, write_bytes, resize_bytes   # file helpers
from swap_utils import byteswap, determine_swap_size         # swap helpers
from log_utils import log                                       # logging helper
from theme_utils import apply_theme, poll_dark_mode            # GUI theme helpers

def launch_gui():
    # --- GUI Setup ---
    root = Tk()
    root.title("N64 Save File Converter")
    root.geometry("730x380")
    root.resizable(False, False)
    root.grid_columnconfigure(0, minsize=180)

    # --- Load N64 logo dynamically ---
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        resources_dir = os.path.join(base_dir, "resources")
        logo_path = os.path.join(resources_dir, "n64_logo.png")
        logo_img = PhotoImage(file=logo_path)
        root.iconphoto(True, logo_img)  # sets window and dock icon
    except Exception:
        logo_img = None

    # --- GUI Variables ---
    input_path = StringVar()
    source_type_var = StringVar()
    source_var = StringVar()
    target_var = StringVar()
    target_type_var = StringVar()
    trim_pad_var = BooleanVar()
    byteswap_var = StringVar(value="None")

    # --- GUI Components ---
    
    # Browse file
    def browse_file():
        path = filedialog.askopenfilename(filetypes=[("N64 Saves", "*.eep *.sra *.fla *.mpk *.srm")])
        if path:
            input_path.set(path)
            selected_type = detect_file_type(path)
            if selected_type in file_types:
                source_type_var.set(selected_type)
            else:
                source_type_var.set("")
    
    Label(root, text="Select N64 Save File:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    directory_entry = Entry(root, textvariable=input_path, width=45)
    directory_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Keep entry scrolled to end
    def scroll_to_end(*args):
        root.after_idle(lambda: directory_entry.xview_moveto(1))
    input_path.trace_add("write", scroll_to_end)
    directory_entry.bind("<KeyRelease>", lambda e: directory_entry.xview_moveto(1))
    directory_entry.bind("<<Paste>>", lambda e: root.after_idle(lambda: directory_entry.xview_moveto(1)))
    
    Button(root, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=5)
    
    # --- Inline log frame ---
    log_frame = Frame(root, bg="#111")
    log_frame.grid(row=0, column=3, rowspan=9, sticky="nsew", padx=5, pady=5)
    root.grid_columnconfigure(3, weight=1)
    
    log_label = Label(log_frame, text="Conversion Log:", bg="#111", fg="#fff")
    log_label.pack(anchor="w", padx=5, pady=(5,0))
    
    log_text_frame = Frame(log_frame, height=200, bg="#111")
    log_text_frame.pack(fill=BOTH, expand=False, padx=5, pady=5)
    
    log_box = Text(log_text_frame, height=25, width=50, wrap="word", bg="#111", fg="#ddd")
    log_box.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar = Scrollbar(log_text_frame, command=log_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    log_box.config(yscrollcommand=scrollbar.set)
    
    # Log tags
    log_box.tag_config("timestamp", foreground="#FFA500")
    log_box.tag_config("level_info", foreground="#FFFFFF")
    log_box.tag_config("level_conversion", foreground="#00FFFF")
    log_box.tag_config("level_warn", foreground="#FFD700")
    log_box.tag_config("level_error", foreground="#FF4500")
    
    # Toggle log window
    log_visible = True
    root.geometry("1000x380")
    
    def toggle_log_window():
        global log_visible
        if log_visible:
            log_frame.grid_remove()
            root.geometry("730x380")
            log_visible = False
        else:
            log_frame.grid()
            root.geometry("1000x380")
            log_visible = True
    
    Button(root, text="Show/Hide Log", command=toggle_log_window).grid(row=7, column=0, pady=15, padx=5)
    
    # Source selection
    Label(root, text="Save File Source Type:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    source_type_label = Label(root, textvariable=source_type_var, relief="flat", width=22, anchor=W)
    source_type_label.grid(row=1, column=1, padx=10, pady=5)
    
    Label(root, text="Save File Source:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    source_menu = ttk.Combobox(root, textvariable=source_var, values=source_list, state="readonly")
    source_menu.grid(row=2, column=1, padx=10, pady=5)
    
    # Target selection
    Label(root, text="Save File Target:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
    target_menu = ttk.Combobox(root, textvariable=target_var, values=target_list, state="readonly")
    target_menu.grid(row=3, column=1, padx=10, pady=5)
    
    Label(root, text="Save File Target Type:").grid(row=4, column=0, sticky=W, padx=10, pady=5)
    target_type_menu = ttk.Combobox(root, textvariable=target_type_var, state="readonly")
    target_type_menu.grid(row=4, column=1, padx=10, pady=5)
    
    # Update target type menu dynamically
    def update_target_type_menu(*args):
        src = source_var.get()
        src_type = source_type_var.get()
        tgt = target_var.get()
        valid_output_types = set()
        if src_type == SRM_LABEL:
            valid_output_types.update([EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL])
        elif src_type in [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL]:
            if tgt in [PJ64_LABEL, WII_LABEL, NATIVE_LABEL]:
                valid_output_types.add(src_type)
            elif tgt == RA_LABEL:
                valid_output_types.add(SRM_LABEL)
        elif src == NATIVE_LABEL:
            if src_type in [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL]:
                valid_output_types.add(src_type)
            elif src_type == SRM_LABEL:
                valid_output_types.add(SRM_LABEL)
        valid_output_types = sorted(valid_output_types)
        target_type_menu['values'] = valid_output_types
        if target_type_var.get() not in valid_output_types:
            target_type_var.set(valid_output_types[0] if valid_output_types else "")
    
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
        if src_type in [SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL]:
            byteswap_menu.config(state="readonly")
            if byteswap_var.get() not in ["Default", "2 bytes", "4 bytes"]:
                byteswap_var.set("Default")
        else:
            byteswap_var.set("Default")
            byteswap_menu.config(state="disabled")
    
    source_type_var.trace_add("write", update_byteswap_menu)
    target_type_var.trace_add("write", update_byteswap_menu)
    
    # Convert button
    Button(root, text="Convert", width=20, command=convert_save).grid(row=7, column=1, pady=15)

    # --- Initialize ---
    update_byteswap_menu()
    update_target_type_menu()
    poll_dark_mode()
    root.mainloop()
