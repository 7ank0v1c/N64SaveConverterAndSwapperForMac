# core/log_utils.py
from datetime import datetime

# Terminal Colours
class TermColors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    ORANGE = "\033[38;5;208m"

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
