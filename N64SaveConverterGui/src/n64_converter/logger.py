# logger.py
from datetime import datetime
from tkinter import END

def log(message, log_box=None, key=None, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    color_map = {
        "INFO": "\033[37m",
        "WARN": "\033[33m",
        "ERROR": "\033[31m"
    }
    print(f"\033[38;5;214m[{timestamp}]\033[0m {color_map.get(level, '\033[37m')}{message}\033[0m")

    if log_box:
        tag = {
            "INFO": "level_info",
            "WARN": "level_warn",
            "ERROR": "level_error"
        }.get(level, "level_info")

        log_box.insert(END, f"[{timestamp}] {message}\n", tag)
        log_box.see(END)
        log_box.update_idletasks()

    with open("conversion_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")