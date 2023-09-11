import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.PluginBase):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)

        # init input, output
        self.input_init("one", "two")
        self.output_init("result")

        self.output_value_set("result", 0)


    def run(self):
        one = self.input_value_get("one")
        two = self.input_value_get("two")

        if not bool(one):
            one = 0

        if not bool(two):
            two = 0

        self.output_value_set("result", float(one) + float(two))