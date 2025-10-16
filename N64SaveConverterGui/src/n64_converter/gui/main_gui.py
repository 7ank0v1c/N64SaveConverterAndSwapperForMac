import os
import tkinter as tk
from tkinter import Frame, Label, Button

# Import system GUIs
from systems.n64.gui.n64_gui_main import setup_n64_gui

# Consoles grouped
CONSOLES_HANDHELD = {
    "Nintendo": ["Game Boy / Game Boy Color", "Game Boy Advance", "Nintendo DS / Nintendo DSi"],
    "Sega": ["Sega GameGear"],
    "Sony": [],
}

CONSOLES_HOME = {
    "Nintendo": ["NES", "SNES", "Nintendo 64", "Nintendo GameCube", "Nintendo Wii"],
    "Sega": ["Sega Master System", "Sega Genesis/Megadrive", "Sega Saturn", "Sega Dreamcast"],
    "Sony": [],
}

# Console → GUI map
CONSOLE_GUI_MAP = {
    "Game Boy / Game Boy Color": None,
    "Game Boy Advance": None,
    "Nintendo DS / Nintendo DSi": None,
    "NES": None,
    "SNES": None,
    "Nintendo 64": setup_n64_gui,
    "Nintendo GameCube": None,
    "Nintendo Wii": None,
    "Sega Master System": None,
    "Sega Genesis/Megadrive": None,
    "Sega Saturn": None,
    "Sega Dreamcast": None,
    "Sega GameGear": None,
}


class TopLevelGUI:
    BASE_WIDTH = 1000
    HEIGHT = 600

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal Save Converter")
        self.root.geometry(f"{self.BASE_WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

        self.logo_frame = None
        self.current_frame = None
        self.console_frame = None

        self.setup_logo()
        self.show_console_selection()
        self.root.mainloop()

    def setup_logo(self):
        """Persistent logo at the top-left"""
        try:
            logo_path = os.path.join(os.getcwd(), "resources", "n64_logo.png")
            self.logo_img = tk.PhotoImage(file=logo_path)
            self.root.iconphoto(True, self.logo_img)
        except Exception as e:
            print(f"Could not load logo: {e}")
            self.logo_img = None

        self.logo_frame = Frame(self.root)
        self.logo_frame.pack(side="top", anchor="w", fill="x")
        self.logo_label = Label(
            self.logo_frame,
            image=self.logo_img if self.logo_img else None,
            text="Universal Save Converter" if not self.logo_img else "",
            compound="left",
            font=("Arial", 16, "bold")
        )
        self.logo_label.pack(anchor="w", padx=10, pady=5)

    def show_console_selection(self):
        """Main console selection screen"""
        self._clear_current_frame()
        if self.console_frame:
            self.console_frame.pack_forget()
        else:
            self.console_frame = Frame(self.root, padx=20, pady=20)

        self.console_frame.pack(side="top", fill="both", expand=True)

        Label(self.console_frame, text="Select Console:", font=("Arial", 16)).pack(pady=(0, 15))

        columns_frame = Frame(self.console_frame)
        columns_frame.pack(fill="x", padx=10)

        # Handheld
        handheld_frame = Frame(columns_frame)
        handheld_frame.pack(side="left", padx=20, anchor="nw")
        Label(handheld_frame, text="Handheld Consoles", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0,5))
        for manufacturer, consoles in CONSOLES_HANDHELD.items():
            if consoles:
                Label(handheld_frame, text=manufacturer, font=("Arial", 12, "italic")).pack(anchor="w", padx=5, pady=(5,0))
            for console in consoles:
                Button(
                    handheld_frame,
                    text=console,
                    width=30,
                    command=lambda c=console: self.load_console_gui(c, CONSOLE_GUI_MAP[c])
                ).pack(padx=10, pady=2, anchor="w")

        # Home
        home_frame = Frame(columns_frame)
        home_frame.pack(side="left", padx=20, anchor="nw")
        Label(home_frame, text="Home Consoles", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0,5))
        for manufacturer, consoles in CONSOLES_HOME.items():
            if consoles:
                Label(home_frame, text=manufacturer, font=("Arial", 12, "italic")).pack(anchor="w", padx=5, pady=(5,0))
            for console in consoles:
                Button(
                    home_frame,
                    text=console,
                    width=30,
                    command=lambda c=console: self.load_console_gui(c, CONSOLE_GUI_MAP[c])
                ).pack(padx=10, pady=2, anchor="w")

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
            # --- Open console GUI in a new Toplevel window ---
            top_window = tk.Toplevel(self.root)
            top_window.title(f"{console_name} Save Converter")
            gui_func(top_window)  # Pass Toplevel as parent

    def _back_to_console_selection(self):
        """Return to console selection screen"""
        self._clear_current_frame()
        self.show_console_selection()

    def _clear_current_frame(self):
        """Destroy current GUI frame if exists"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None


if __name__ == "__main__":
    TopLevelGUI()