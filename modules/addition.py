import tkinter as tk
from tkinter import ttk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)

        # init input, output
        self.input_init("one", "two")
        self.output_init("result")

        self.input_value_set("one", 0)
        self.input_value_set("two", 0)
        self.output_value_set("result", 0)

        self.run()


    def run(self):
        self.output_value_set("result", float(self.input_value_get("one")) + float(self.input_value_get("two")))
