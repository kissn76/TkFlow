import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, plugin_id, pluginframe_object, canvas_object, **kwargs):
        super().__init__(plugin_id, pluginframe_object, canvas_object, **kwargs)

        # init input, output
        self.input_init("one", "two")
        self.output_init("result")

        # init own plugin
        self.content_set()

        # set input, output init values
        self.output_value_set("result", 0)


    def content_set(self):
        self.marker_widget = ttk.Label(self.view_get(), text=f"{self.pluginframe_get().id_get()}-{self.id_get()}")

        self.view_init()
        self.content_init(self.marker_widget)


    def run(self):
        one = self.input_value_get_referenced("one")
        two = self.input_value_get_referenced("two")

        if not bool(one):
            one = 0

        if not bool(two):
            two = 0

        self.output_value_set("result", float(one) + float(two))
