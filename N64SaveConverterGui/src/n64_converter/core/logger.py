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

    # --- Terminal colors ---
    term_color_map = {
        "INFO": TermColors.WHITE,
        "WARN": TermColors.YELLOW,
        "ERROR": TermColors.RED,
        "SUCCESS": TermColors.GREEN,  # new success color
    }
    conversion_color = TermColors.BLUE
    timestamp_color = TermColors.ORANGE
    reset = TermColors.RESET

    # --- Terminal output ---
    if "Using conversion table entry" in message:
        print(f"{timestamp_color}[{timestamp}]{reset} {conversion_color}{message}{reset}")
    else:
        print(f"{timestamp_color}[{timestamp}]{reset} {term_color_map.get(level, TermColors.WHITE)}{message}{reset}")

    # --- GUI log ---
    if log_box:
        if "Using conversion table entry" in message:
            tag = "level_conversion"  # orange
        else:
            tag = {
                "INFO": "level_info",
                "WARN": "level_warn",
                "ERROR": "level_error",
                "SUCCESS": "level_success",  # new GUI tag
            }.get(level, "level_info")

        gui_message = f"[{timestamp}] {message}"
        gui_log(log_box, gui_message, level=tag)

    # --- Log to file ---
    with open("conversion_log.txt", "a") as f:
        f.write(f"[{timestamp}]" + (f" [{key}]" if key else "") + f" {message}\n")
