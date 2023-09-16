import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class SettingsWindow(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
