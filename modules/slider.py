import tkinter as tk
from tkinter import ttk


class Plugin(ttk.Scale):
    def __init__(self, master, **kwargs):
        super(Plugin, self).__init__(master=master, from_=0, to=100, orient='horizontal', **kwargs)
