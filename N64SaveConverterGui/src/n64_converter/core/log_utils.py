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

# GUI logging
def gui_log(log_box, message, level="info"):
    tags = {
        "info": "level_info",
        "conversion": "level_conversion",
        "warn": "level_warn",
        "error": "level_error"
    }
    timestamp = datetime.now().strftime("[%H:%M:%S] ")
    log_box.insert("end", timestamp, "timestamp")
    log_box.insert("end", message + "\n", tags.get(level, "level_info"))
    log_box.see("end")  # auto-scroll
