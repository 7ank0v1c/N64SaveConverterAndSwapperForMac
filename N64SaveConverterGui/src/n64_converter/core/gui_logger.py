# core/gui_logger.py

from core.log_utils import gui_log

# Pastel colors used for GUI log message tags
PASTEL_GUI_COLORS = {
    "info": "#a8c7fa",     # soft blue
    "success": "#9ae8a4",  # soft green
    "warn": "#ffd580",      # pastel orange
    "error": "#ff9b9b",     # light red
    "conversion": "#7FFFD4" # aqua
}

# Keep a reference to the active Text widget
log_widget = None

def set_log_widget(widget):
    """Assign the GUI log Text widget so all logging functions can write to it."""
    global log_widget
    log_widget = widget

    # Configure pastel color tags on the widget
    for tag, color in PASTEL_GUI_COLORS.items():
        log_widget.tag_config(tag, foreground=color, background="#111")


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
