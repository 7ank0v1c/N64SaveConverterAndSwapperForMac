# core/gui_logger.py

from core.log_utils import gui_log

# Keep a reference to the active Text widget
log_widget = None

def set_log_widget(widget):
    """Assign the GUI log Text widget so all logging functions can write to it."""
    global log_widget
    log_widget = widget


def info(msg):
    """Log an informational message."""
    if log_widget:
        gui_log(log_widget, msg, level="info")


def success(msg):
    """Log a success message."""
    if log_widget:
        gui_log(log_widget, msg, level="success")


def error(msg):
    """Log an error message."""
    if log_widget:
        gui_log(log_widget, msg, level="error")


def warn(msg):
    """Log a warning message."""
    if log_widget:
        gui_log(log_widget, msg, level="warn")


def conversion(msg):
    """Log a conversion-related message."""
    if log_widget:
        gui_log(log_widget, msg, level="conversion")
