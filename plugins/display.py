import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        # init input, output, setting variables
        self.inputvariable_init("in")

        # init own plugin view
        self.show = ttk.Label(self, text="")
        self.contentrow_init(self.show)


    def run(self):
        inp = self.input_value_get("in")

        if not bool(inp):
            inp = 0

        self.show.configure(text=str(inp))
