import tkinter as tk
from tkinter import ttk


class WidgetBase():
    def __init__(self, master):
        self.frame = ttk.Frame(master=master)
