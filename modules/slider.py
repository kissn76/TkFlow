import tkinter as tk
from tkinter import ttk


class Plugin(ttk.Scale):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(from_=0, to=100, orient='horizontal', **kwargs)
