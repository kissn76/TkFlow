'''
Demo plugin
It creates list array from dynamically growing input
'''

import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        # init input, output, setting variables
        self.inputlist_init(input_id_prefix="input", max_element=0, setting_enabled=True)
        self.outputvariable_init("result", [])

        # init own plugin view
        self.show = ttk.Label(self, text="")
        self.contentrow_init(self.show, "result")


    def run(self):
        out = []
        for input_id, input_reference_id in self.inputlist_get("input").items():
            if not input_reference_id == None:
                value = self.input_value_get(input_id)
                out.append(value)

        self.outputvariable_set("result", out)
        self.show.configure(text=str(self.outputvariable_get("result")))
