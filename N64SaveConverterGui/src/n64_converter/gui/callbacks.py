# gui/callbacks.py

from tkinter import filedialog
from core.file_utils import detect_file_type
from core.logger import log

def browse_file(filetypes, path_var, type_var=None):
    """
    Opens a file dialog to select a file.
    Optionally sets type_var using detect_file_type.
    """
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path:
        path_var.set(path)
        if type_var:
            selected_type = detect_file_type(path)
            type_var.set(selected_type if selected_type else "")

def update_combobox_values(combobox, values, default=None):
    """
    Updates a combobox with new values.
    Sets default selection if provided or first value.
    """
    combobox['values'] = values
    if default:
        combobox.set(default)
    elif values:
        combobox.set(values[0])
    else:
        combobox.set("")

def toggle_widget_visibility(widget, window, visible_flag, shrink_geometry=None, expand_geometry=None):
    """
    Shows/hides a widget and resizes window if needed.
    Returns the updated visible_flag.
    """
    if visible_flag:
        widget.grid_remove()
        if shrink_geometry:
            window.geometry(shrink_geometry)
        return False
    else:
        widget.grid()
        if expand_geometry:
            window.geometry(expand_geometry)
        return True

def safe_log(message, log_box=None, level="INFO"):
    """
    Logs message to a Text widget safely.
    """
    log(message, level=level, log_box=log_box)
