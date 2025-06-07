import tkinter as tk
import sv_ttk
from GUI import GUI
from Limiter import Controller
import os

root = tk.Tk()
root.iconbitmap(os.path.join(os.path.dirname(__file__), "favicon.ico"))
sv_ttk.set_theme("dark")
gui = GUI(root)
controller = Controller()

gui.set_controller(controller)
controller.set_gui(gui)

def save_window_geometry():
    with open("window_geometry.txt", "w") as f:
        f.write(root.geometry())

def load_window_geometry():
    if os.path.exists("window_geometry.txt"):
        with open("window_geometry.txt", "r") as f:
            geometry = f.read().strip()
            if geometry:
                root.geometry(geometry)

def main():
    root.title("Ultimate File Converter")
    load_window_geometry()
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

def on_close():
    save_window_geometry()
    root.destroy()

if __name__ == "__main__":
    main()
