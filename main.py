import tkinter as tk
from SmartHomeGUI import SmartHomeGUI


if __name__ == "__main__":
    # Create the main GUI window
    root = tk.Tk()
    app = SmartHomeGUI(root)

    window_width = 1100
    window_height = 450

    # Screen dimensions
    screen_width = 1920
    screen_height = 1080

    # Calculate the center position
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)

    # Set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # Keep the window displaying
    root.mainloop()
