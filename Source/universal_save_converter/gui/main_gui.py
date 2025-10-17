# gui/main_gui.py

import os
import tkinter as tk
from tkinter import Frame, Label, Button

# Import system GUIs
from systems.n64.gui.n64_gui_main import setup_n64_gui
from systems.gba.gui.gba_gui_main import setup_gba_gui

# Consoles grouped by manufacturer
NINTENDO_HOME = ["NES", "SNES", "Nintendo 64", "Nintendo Virtual Boy", "Nintendo GameCube", "Nintendo Wii"]
NINTENDO_HANDHELD = ["Game Boy / Game Boy Color", "Game Boy Advance", "Nintendo DS / Nintendo DSi"]

SEGA_HOME = ["Sega Master System", "Sega Genesis/Megadrive", "Sega Saturn", "Sega Dreamcast"]
SEGA_HANDHELD = ["Sega GameGear"]

SONY_HOME = ["Sony PlayStation", "Sony PlayStation 2"]
SONY_HANDHELD = ["Sony PlayStation Portable", "Sony PlayStation Vita"]

PASTEL_DARK_BLUE = "#4A6FA5"
PASTEL_HOVER_BLUE = "#5E84B8"
TEXT_COLOR = "#1E3A5F"

# Console → GUI map
CONSOLE_GUI_MAP = {
    "Game Boy / Game Boy Color": None,
    "Game Boy Advance": setup_gba_gui,
    "Nintendo DS / Nintendo DSi": None,
    "NES": None,
    "SNES": None,
    "Nintendo 64": setup_n64_gui,
    "Nintendo Virtual Boy": None,
    "Nintendo GameCube": None,
    "Nintendo Wii": None,
    "Sega Master System": None,
    "Sega Genesis/Megadrive": None,
    "Sega Saturn": None,
    "Sega Dreamcast": None,
    "Sega GameGear": None,
    "Sony PlayStation": None,
    "Sony PlayStation 2": None,
    "Sony PlayStation Portable": None,
    "Sony PlayStation Vita": None,
}


class TopLevelGUI:
    BASE_WIDTH = 930
    HEIGHT = 600
    VERTICAL_OFFSET = 100  # adjust vertical positioning

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal Save Converter")
        self.root.resizable(False, False)

        self.toplevel_windows = []  # <--- Track opened Toplevels

        # --- Center window horizontally and slightly higher vertically ---
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.BASE_WIDTH) // 2
        y = (screen_height - self.HEIGHT) // 2 - self.VERTICAL_OFFSET
        self.root.geometry(f"{self.BASE_WIDTH}x{self.HEIGHT}+{x}+{y}")

        self.logo_frame = None
        self.current_frame = None
        self.console_frame = None

        # Compute uniform button width
        self.button_width = self._calculate_button_width()

        self.setup_logo()
        self.show_console_selection()
        self.root.mainloop()

    def _calculate_button_width(self):
        """Calculate a uniform button width based on the longest console name"""
        all_names = NINTENDO_HOME + NINTENDO_HANDHELD + SEGA_HOME + SEGA_HANDHELD + SONY_HOME + SONY_HANDHELD
        longest_name = max(all_names, key=len)
        return len(longest_name) + 2

    def setup_logo(self):
        """Persistent centered logo at the top, fallback to text if not found"""
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logo_path = os.path.join(project_root, "resources", "new_usc_logo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(True, self.logo_img)
        except Exception as e:
            print(f"Could not load logo: {e}")
            self.logo_img = None

        self.logo_frame = Frame(self.root)
        self.logo_frame.pack(side="top", fill="x", pady=10)

        self.logo_label = Label(
            self.logo_frame,
            image=self.logo_img if self.logo_img else None,
            text="Universal Save Converter" if not self.logo_img else "",
            compound="left",
            font=("Arial", 16, "bold")
        )
        self.logo_label.pack(anchor="center")  # Center horizontally

    def _add_hover_effect(self, button):
        """Add hover effect to a button"""
        button.bind("<Enter>", lambda e: button.config(bg=PASTEL_HOVER_BLUE))
        button.bind("<Leave>", lambda e: button.config(bg=PASTEL_DARK_BLUE))

    def show_console_selection(self):
        """Main console selection screen with manufacturer columns"""
        self._clear_current_frame()
        if self.console_frame:
            self.console_frame.destroy()
        self.console_frame = Frame(self.root, padx=20, pady=20)
        self.console_frame.pack(side="top", fill="both", expand=True)

        Label(
            self.console_frame,
            text="Select Console:",
            font=("Arial", 30, "bold")
        ).pack(pady=(0, 15))

        grid_frame = Frame(self.console_frame)
        grid_frame.pack(fill="both", expand=True)

        manufacturers = [
            ("Nintendo", NINTENDO_HOME, NINTENDO_HANDHELD),
            ("Sega", SEGA_HOME, SEGA_HANDHELD),
            ("Sony", SONY_HOME, SONY_HANDHELD),
        ]

        for col_index, (name, home_list, handheld_list) in enumerate(manufacturers):
            Label(grid_frame, text=name, font=("Arial", 14, "bold")).grid(row=0, column=col_index, padx=20, pady=(0, 5), sticky="w")
            row = 1
            for console in home_list + handheld_list:
                btn = Button(
                    grid_frame,
                    text=console,
                    width=self.button_width,
                    command=lambda c=console: self.load_console_gui(c, CONSOLE_GUI_MAP.get(c)),
                    bg=PASTEL_DARK_BLUE,
                    fg=TEXT_COLOR,
                    activebackground=PASTEL_HOVER_BLUE,
                    activeforeground=TEXT_COLOR,
                    relief="flat"
                )
                btn.grid(row=row, column=col_index, padx=5, pady=2, sticky="w")
                self._add_hover_effect(btn)
                row += 1

    def load_console_gui(self, console_name, gui_func):
        """Load console GUI in a Toplevel window for full functionality"""
        self._clear_current_frame()
        if self.console_frame:
            self.console_frame.pack_forget()

        self.current_frame = Frame(self.root)
        self.current_frame.pack(side="top", fill="both", expand=True)

        back_btn = Button(
            self.current_frame,
            text="Back",
            width=10,
            command=self._back_to_console_selection,
            bg=PASTEL_DARK_BLUE,
            fg=TEXT_COLOR,
            activebackground=PASTEL_HOVER_BLUE,
            activeforeground=TEXT_COLOR,
            relief="flat"
        )
        back_btn.pack(anchor="nw", pady=(0, 10), padx=10)
        self._add_hover_effect(back_btn)

        if gui_func is None:
            Label(
                self.current_frame,
                text=f"{console_name} Coming Soon...",
                font=("Arial", 14)
            ).pack(pady=50)
        else:
            top_window = tk.Toplevel(self.root)
            self.toplevel_windows.append(top_window)
            top_window.title(f"{console_name} Save Converter")

            top_window.update_idletasks()
            win_width = top_window.winfo_width()
            win_height = top_window.winfo_height()
            screen_width = top_window.winfo_screenwidth()
            screen_height = top_window.winfo_screenheight()
            x = (screen_width - win_width) // 2
            y = (screen_height - win_height) // 2 - self.VERTICAL_OFFSET
            top_window.geometry(f"+{x}+{y}")

            gui_func(top_window)

    def _back_to_console_selection(self):
        for win in self.toplevel_windows:
            if win.winfo_exists():
                win.destroy()
        self.toplevel_windows.clear()

        self._clear_current_frame()
        self.show_console_selection()

    def _clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    TopLevelGUI()