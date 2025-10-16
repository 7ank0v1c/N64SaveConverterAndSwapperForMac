# core/gui_logger.py
from datetime import datetime
from core.log_utils import gui_log, PASTEL_GUI_COLORS

# Global reference to the active Text widget
log_widget = None

def set_log_widget(widget):
    """Assign the GUI log Text widget for logging."""
    global log_widget
    log_widget = widget

    # Configure pastel color tags on the widget
    for tag, color in PASTEL_GUI_COLORS.items():
        log_widget.tag_config(tag, foreground=color, background="#111")

def _log(msg, level="level_info"):
    """Internal helper to log with timestamp to the global log widget."""
    if not log_widget:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Insert timestamp with its tag
    log_widget.insert("end", f"[{timestamp}] ", "timestamp")
    # Insert message
    gui_log(log_widget, msg, level=level)

# Convenience functions
def info(msg):       _log(msg, level="level_info")
def success(msg):    _log(msg, level="level_success")
def warn(msg):       _log(msg, level="level_warn")
def error(msg):      _log(msg, level="level_error")
def conversion(msg): _log(msg, level="level_conversion")
