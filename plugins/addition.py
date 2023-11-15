'''
Demo plugin
It sums the parts of the list input array.
It has view part. Show the value of the input and output.
'''

import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        # init input, output, setting variables
        self.inputvariable_init("input", [])
        self.outputvariable_init("result", 0)

        # init own plugin view
        self.show = ttk.Label(self, text="")
        self.contentrow_init(self.show, "result")


    def run(self):
        out = 0
        input_values = self.input_value_get("input")
        if isinstance(input_values, list):
            for input_value in input_values:
                if isinstance(input_value, int) or isinstance(input_value, float):
                    out += input_value

        self.outputvariable_set("result", float(out))

        self.show.configure(text=str(self.outputvariable_get("result")))
