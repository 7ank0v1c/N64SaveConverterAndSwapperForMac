# main.py
import sys
from core.logger import setup_logging, log
from gui import launch_gui

def main():
    # Initialize logging
    setup_logging()

    # Launch GUI
    launch_gui()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] Application crashed: {e}", file=sys.stderr)
        sys.exit(1)
