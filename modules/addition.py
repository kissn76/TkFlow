import tkinter as tk
from tkinter import ttk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)

        # init input, output
        self.input_init("one", "two")
        self.output_init("result")


    def output_set(self):
        self.output_value_set("result", float(self.input_value_get("one")) + float(self.input_value_get("two")))
