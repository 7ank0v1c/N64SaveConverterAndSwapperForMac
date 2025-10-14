# log_utils.py
from datetime import datetime

def log(log_box, message, key=None, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    term_color_map = {
        "INFO": "\033[37m",
        "WARN": "\033[33m",
        "ERROR": "\033[31m",
    }
    conversion_color = "\033[36m"
    timestamp_color = "\033[38;5;214m"
    reset = "\033[0m"

    # Console
    if "Using conversion table entry" in message:
        print(f"{timestamp_color}[{timestamp}]{reset} {conversion_color}{message}{reset}")
    else:
        print(f"{timestamp_color}[{timestamp}]{reset} {term_color_map.get(level, '\033[37m')}{message}{reset}")

    # GUI log
    if log_box:
        tag = {
            "INFO": "level_info",
            "WARN": "level_warn",
            "ERROR": "level_error"
        }.get(level, "level_info")

        if "Using conversion table entry" in message:
            tag = "level_conversion"

        log_box.insert("end", f"[{timestamp}]", "timestamp")
        if key and "Using conversion table entry" not in message:
            log_box.insert("end", f" [{key}]")
        log_box.insert("end", f" {message}\n", tag)
        log_box.see("end")
        log_box.update_idletasks()

    # File
    with open("conversion_log.txt", "a") as f:
        f.write(f"[{timestamp}]" + (f" [{key}]" if key else "") + f" {message}\n")