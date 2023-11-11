import tkinter as tk
from SmartHomeGUI import SmartHomeGUI


if __name__ == "__main__":
    # Create the main GUI window
    root = tk.Tk()
    app = SmartHomeGUI(root)

    # Start the main GUI loop
    root.mainloop()
