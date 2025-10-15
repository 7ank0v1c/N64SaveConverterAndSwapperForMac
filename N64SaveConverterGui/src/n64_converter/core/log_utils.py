# core/log_utils.py
from datetime import datetime

# Terminal Colours
class TermColors:
    RESET = "\033[0m"
    RED = "\033[38;5;203m"       # pastel red
    GREEN = "\033[38;5;120m"     # soft green
    YELLOW = "\033[38;5;227m"    # pastel yellow
    BLUE = "\033[38;5;117m"      # pastel blue
    MAGENTA = "\033[38;5;177m"   # pastel magenta
    CYAN = "\033[38;5;159m"      # pastel cyan
    WHITE = "\033[38;5;255m"     # bright white
    ORANGE = "\033[38;5;215m"    # soft orange

# Map pastel colours for GUI text
PASTEL_GUI_COLORS = {
    "timestamp": "#FFD8A8",        # ORANGE
    "level_info": "#FFFFFF",       # WHITE
    "level_conversion": "#7FFFD4", # CYAN
    "level_warn": "#FFFACD",       # YELLOW
    "level_error": "#FF7F7F",      # RED
    "level_success": "#90EE90"     # GREEN
}

# GUI logging
def gui_log(log_box, message, level="info"):
    """
    Inserts a message into the GUI log box.
    Assumes `message` already contains timestamp (from logger.py).
    """
    tags = {
        "info": "level_info",
        "conversion": "level_conversion",
        "warn": "level_warn",
        "error": "level_error",
        "success": "level_success"
    }

    # Insert the message as-is; no extra timestamp
    log_box.insert("end", message + "\n", tags.get(level, "level_info"))
    log_box.see("end")  # auto-scroll

    # Force GUI update immediately so logs appear live
    log_box.update_idletasks()
