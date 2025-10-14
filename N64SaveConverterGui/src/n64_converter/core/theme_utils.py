# core/theme_util.py
import platform
import subprocess
import tkinter as tk

current_mode = None  # module-level variable

def is_dark_mode():
    """
    Returns True if macOS is in Dark Mode.
    On other systems, defaults to False.
    """
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True, text=True
            )
            return result.stdout.strip().lower() == "dark"
        except Exception:
            return False
    return False

def detect_widgets(root):
    """
    Automatically detect labels, text widgets (log boxes), and frames in the GUI.
    Returns a dict with keys: 'labels', 'log_box', 'log_frame', 'log_label'.
    """
    widgets = {"labels": [], "log_box": None, "log_frame": None, "log_label": None}
    
    def recurse_children(parent):
        for child in parent.winfo_children():
            # Labels
            if isinstance(child, tk.Label):
                widgets["labels"].append(child)
            # Text widgets (assuming log_box)
            elif isinstance(child, tk.Text):
                widgets["log_box"] = child
            # Frames (assuming log_frame)
            elif isinstance(child, tk.Frame):
                widgets["log_frame"] = child
            # Recursive check
            recurse_children(child)
    
    recurse_children(root)
    # Optional: detect a label for log_label (maybe first label in log_frame)
    if widgets["log_frame"] and widgets["log_frame"].winfo_children():
        for child in widgets["log_frame"].winfo_children():
            if isinstance(child, tk.Label):
                widgets["log_label"] = child
                break
    return widgets

def apply_theme(root, widgets=None, dark=None):
    """
    Apply light/dark theme to the GUI.
    If widgets is None, automatically detects them.
    """
    if widgets is None:
        widgets = detect_widgets(root)

    if dark is None:
        dark = is_dark_mode()

    colors = {
        "bg": "#111" if dark else "#fff",
        "fg": "#ddd" if dark else "#000",
        "label_bg": "#111" if dark else "#fff",
        "label_fg": "#fff" if dark else "#000",
        "log_tag_info": "#FFF" if dark else "#000",
        "log_tag_conversion": "#0FF" if dark else "#008B8B",
        "log_tag_warn": "#FFD700" if dark else "#B8860B",
        "log_tag_error": "#FF4500" if dark else "#B22222",
        "log_tag_timestamp": "#FFA500" if dark else "#FF8C00",
    }

    # Root background
    root.configure(bg=colors["bg"])

    # Labels
    for lbl in widgets.get("labels", []):
        lbl.configure(bg=colors["label_bg"], fg=colors["label_fg"])

    # Log frame & box
    if widgets.get("log_frame"):
        widgets["log_frame"].configure(bg=colors["bg"])
    if widgets.get("log_box"):
        log_box = widgets["log_box"]
        log_box.configure(bg=colors["bg"], fg=colors["fg"])
        log_box.tag_config("timestamp", foreground=colors["log_tag_timestamp"])
        log_box.tag_config("level_info", foreground=colors["log_tag_info"])
        log_box.tag_config("level_conversion", foreground=colors["log_tag_conversion"])
        log_box.tag_config("level_warn", foreground=colors["log_tag_warn"])
        log_box.tag_config("level_error", foreground=colors["log_tag_error"])
    if widgets.get("log_label"):
        widgets["log_label"].configure(bg=colors["bg"], fg=colors["fg"])

def start_polling(root, widgets=None, interval=1000):
    """
    Polls for dark/light mode changes and reapplies theme.
    """
    global current_mode
    dark = is_dark_mode()
    if dark != current_mode:
        current_mode = dark
        apply_theme(root, widgets, dark)
    root.after(interval, start_polling, root, widgets, interval)
