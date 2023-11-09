import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        self.show_1 = None
        self.show_2 = None
        self.show_r = None

        # init input, output
        self.inputvariable_init("one")
        self.inputvariable_init("two")
        self.outputvariable_init("result")

        # init own plugin
        self.content_init()

        # set input, output init values
        self.outputvariable_set("result", 0)


    def content_init(self):
        self.show_1 = ttk.Label(self, text="")
        self.show_2 = ttk.Label(self, text="")
        self.show_r = ttk.Label(self, text="")

        self.contentrow_init(self.show_1)
        self.contentrow_init(self.show_2)
        self.contentrow_init(self.show_r)


    def run(self):
        one = self.input_value_get("one")
        two = self.input_value_get("two")

        if not bool(one):
            one = 0

        if not bool(two):
            two = 0

        self.outputvariable_set("result", float(one) + float(two))

        self.show_1.configure(text=str(one))
        self.show_2.configure(text=str(two))
        self.show_r.configure(text=str(self.outputvariable_get("result")))
