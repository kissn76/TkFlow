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
        self.inputvariable_init("one")
        self.inputvariable_init("two")
        self.outputvariable_init("result", 0)

        # init own plugin view
        self.show_1 = ttk.Label(self, text="")
        self.show_2 = ttk.Label(self, text="")
        self.show_r = ttk.Label(self, text="")
        self.contentrow_init(self.show_1, "in_1")
        self.contentrow_init(self.show_2, "in_2")
        self.contentrow_init(self.show_r, "out")


    def run(self):
        one = self.input_value_get("one")
        if not bool(one):
            one = 0

        two = self.input_value_get("two")
        if not bool(two):
            two = 0

        self.outputvariable_set("result", float(one) + float(two))

        self.show_1.configure(text=str(one))
        self.show_2.configure(text=str(two))
        self.show_r.configure(text=str(self.outputvariable_get("result")))
