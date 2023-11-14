'''
Demo plugin with two input and one output.
It has view part. Show the value of the input and output.
'''

import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        # init input, output, setting variables
        self.inputvariable_init("input_1", 0)
        self.inputvariable_init("input_2", 0)
        self.outputvariable_init("result", 0)

        # init own plugin view
        # self.show_1 = ttk.Label(self, text="")
        self.show_r = ttk.Label(self, text="")
        # self.contentrow_init(self.show_1, "input")
        self.contentrow_init(self.show_r, "result")


    def run(self):
        out = 0
        input = self.inputvariable_get()
        if bool(input):
            for input_id, input_value in input.items():
                out += self.input_value_get(input_value)

        self.outputvariable_set("result", float(out))

        # self.show_1.configure(text=str(input))
        self.show_r.configure(text=str(self.outputvariable_get("result")))
