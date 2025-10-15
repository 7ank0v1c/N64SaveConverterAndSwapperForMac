# core/logger.py

import os
from datetime import datetime
from core.log_utils import TermColors, gui_log

def setup_logging():
    """Ensure log file exists."""
    if not os.path.exists("conversion_log.txt"):
        with open("conversion_log.txt", "w") as f:
            f.write("=== Conversion Log Initialized ===\n")

def log(message, log_box=None, key=None, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Determine terminal colour ---
    term_color_map = {
        "INFO": TermColors.WHITE,
        "WARN": TermColors.YELLOW,
        "ERROR": TermColors.RED,
    }
    conversion_color = TermColors.CYAN
    timestamp_color = TermColors.YELLOW
    reset = TermColors.RESET

    # --- Terminal output ---
    if "Using conversion table entry" in message:
        print(f"{timestamp_color}[{timestamp}]{reset} {conversion_color}{message}{reset}")
    else:
        print(f"{timestamp_color}[{timestamp}]{reset} {term_color_map.get(level, TermColors.WHITE)}{message}{reset}")

    # --- GUI log (if provided) ---
    if log_box:
        tag = "level_info"
        if level == "WARN":
            tag = "level_warn"
        elif level == "ERROR":
            tag = "level_error"
        elif "Using conversion table entry" in message:
            tag = "level_conversion"

        timestamp_display = f"[{timestamp}]"
        if key and "Using conversion table entry" not in message:
            gui_message = f"{timestamp_display} [{key}] {message}"
        else:
            gui_message = f"{timestamp_display} {message}"

        gui_log(log_box, gui_message, level=tag.replace("level_", ""))

    # --- Log to file ---
    with open("conversion_log.txt", "a") as f:
        f.write(f"[{timestamp}]" + (f" [{key}]" if key else "") + f" {message}\n")
