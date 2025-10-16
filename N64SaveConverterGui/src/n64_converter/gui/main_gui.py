# gui/main_gui.py

import os
import tkinter as tk
from tkinter import Frame, Label, Button

# Import system GUIs
from systems.n64.gui.n64_gui_main import setup_n64_gui

# Consoles grouped by manufacturer
NINTENDO_HOME = ["NES", "SNES", "Nintendo 64", "Nintendo Virtual Boy", "Nintendo GameCube", "Nintendo Wii"]
NINTENDO_HANDHELD = ["Game Boy / Game Boy Color", "Game Boy Advance", "Nintendo DS / Nintendo DSi"]

SEGA_HOME = ["Sega Master System", "Sega Genesis/Megadrive", "Sega Saturn", "Sega Dreamcast"]
SEGA_HANDHELD = ["Sega GameGear"]

SONY_HOME = ["Sony PlayStation", "Sony PlayStation 2"]
SONY_HANDHELD = ["Sony PlayStation Portable", "Sony PlayStation Vita"]

# Console → GUI map
CONSOLE_GUI_MAP = {
    "Game Boy / Game Boy Color": None,
    "Game Boy Advance": None,
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
        """Persistent logo at the top-left with centered big bold title"""
        try:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            logo_path = os.path.join(project_root, "resources", "usc_logo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(True, self.logo_img)
        except Exception as e:
            print(f"Could not load logo: {e}")
            self.logo_img = None

        self.logo_frame = Frame(self.root)
        self.logo_frame.pack(side="top", fill="x", pady=10)

        # Logo on the left
        if self.logo_img:
            self.logo_label = Label(self.logo_frame, image=self.logo_img)
            self.logo_label.grid(row=0, column=0, padx=10, sticky="w")
        else:
            self.logo_label = Label(self.logo_frame, text="Universal Save Converter", font=("Arial", 16, "bold"))
            self.logo_label.grid(row=0, column=0, padx=10, sticky="w")

        # Big centered title
        self.title_label = Label(
            self.logo_frame,
            text="Universal Save Converter",
            font=("Arial", 32, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=200)  # Centered with padding
        self.logo_frame.grid_columnconfigure(0, weight=1)  # logo column can shrink
        self.logo_frame.grid_columnconfigure(1, weight=1)  # title column centers
        
    def show_console_selection(self):
        """Main console selection screen with manufacturer columns"""
        self._clear_current_frame()
        if self.console_frame:
            self.console_frame.destroy()  # destroy old widgets
        self.console_frame = Frame(self.root, padx=20, pady=20)
        self.console_frame.pack(side="top", fill="both", expand=True)

        # --- Select Console label below ---
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

        # Determine max rows needed for any column
        max_rows = max(len(home) + len(handheld) for _, home, handheld in manufacturers)

        # Populate columns by manufacturer
        for col_index, (name, home_list, handheld_list) in enumerate(manufacturers):
            Label(grid_frame, text=name, font=("Arial", 14, "bold")).grid(row=0, column=col_index, padx=20, pady=(0,5), sticky="w")
            row = 1
            # Home consoles
            for console in home_list:
                Button(
                    grid_frame,
                    text=console,
                    width=self.button_width,
                    command=lambda c=console: self.load_console_gui(c, CONSOLE_GUI_MAP.get(c))
                ).grid(row=row, column=col_index, padx=5, pady=2, sticky="w")
                row += 1
            # Handheld consoles below
            for console in handheld_list:
                Button(
                    grid_frame,
                    text=console,
                    width=self.button_width,
                    command=lambda c=console: self.load_console_gui(c, CONSOLE_GUI_MAP.get(c))
                ).grid(row=row, column=col_index, padx=5, pady=2, sticky="w")
                row += 1

    def load_console_gui(self, console_name, gui_func):
        """Load console GUI in a Toplevel window for full functionality"""
        self._clear_current_frame()
        if self.console_frame:
            self.console_frame.pack_forget()

        self.current_frame = Frame(self.root)
        self.current_frame.pack(side="top", fill="both", expand=True)

        # Back button
        Button(
            self.current_frame,
            text="Back",
            width=10,
            command=self._back_to_console_selection
        ).pack(anchor="nw", pady=(0,10), padx=10)

        if gui_func is None:
            Label(
                self.current_frame,
                text=f"{console_name} GUI not implemented yet.",
                font=("Arial", 14)
            ).pack(pady=50)
        else:
            top_window = tk.Toplevel(self.root)
            self.toplevel_windows.append(top_window)  # <--- Track Toplevel
            top_window.title(f"{console_name} Save Converter")

            # --- Center Toplevel window horizontally and slightly higher vertically ---
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
        # Destroy all Toplevel windows
        for win in self.toplevel_windows:
            if win.winfo_exists():
                win.destroy()
        self.toplevel_windows.clear()  # reset list

        self._clear_current_frame()
        self.show_console_selection()

    def _clear_current_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    TopLevelGUI()