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
        self.settingvariable_init("max", None)
        self.inputlist_init("input", self.settingvariable_get("max"))
        self.outputvariable_init("result", [])

        # init settings view
        self.settingsview_get().savebtn_configure(self.content_set)
        self.settingrow_init("entry", "max", "Max number of elements")

        # init own plugin view
        self.show = ttk.Label(self, text="")
        self.contentrow_init(self.show, "result")


    def content_set(self):
        self.setting_save()

        self.inputlist_max_element_set("input", self.settingvariable_get("max"))


    def run(self):
        out = []
        for input_id, input_reference_id in self.inputlist_get("input").items():
            if not input_reference_id == None:
                value = self.input_value_get(input_id)
                out.append(value)

        self.outputvariable_set("result", out)
        self.show.configure(text=str(self.outputvariable_get("result")))
