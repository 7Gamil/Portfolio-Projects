import pyautogui
import tkinter as tk
from tkinter import Label, Button
import time

class MousePositionFinder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mouse Position Finder")
        self.root.geometry("300x150")
        
        # Create label to display coordinates
        self.pos_label = Label(self.root, text="Current Position: (0, 0)")
        self.pos_label.pack(pady=10)
        
        # Create start/stop button
        self.running = False
        self.button = Button(self.root, text="Start Tracking", command=self.toggle_tracking)
        self.button.pack(pady=10)
        
        # Create instructions label
        instructions = """
        1. Click 'Start Tracking'
        2. Move mouse to desired position
        3. Press Ctrl+C in terminal to stop
        """
        self.instructions_label = Label(self.root, text=instructions)
        self.instructions_label.pack(pady=10)

    def toggle_tracking(self):
        if not self.running:
            self.running = True
            self.button.config(text="Stop Tracking")
            self.track_mouse()
        else:
            self.running = False
            self.button.config(text="Start Tracking")

    def track_mouse(self):
        if self.running:
            x, y = pyautogui.position()
            self.pos_label.config(text=f"Current Position: ({x}, {y})")
            self.root.after(100, self.track_mouse)  # Update every 100ms

    def run(self):
        self.root.mainloop()

# Usage
if __name__ == "__main__":
    # Fail-safe feature: quickly move mouse to corner to stop script
    pyautogui.FAILSAFE = True
    
    finder = MousePositionFinder()
    finder.run()