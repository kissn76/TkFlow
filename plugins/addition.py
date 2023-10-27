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
        self.content_set(pluginframe_object)

        # set input, output init values
        self.output_value_set("result", 0)


    def content_set(self, pluginframe_object):
        self.view_create(pluginframe_object)
        self.view_init()


    def run(self):
        one = self.input_value_get_referenced("one")
        two = self.input_value_get_referenced("two")

        if not bool(one):
            one = 0

        if not bool(two):
            two = 0

        self.output_value_set("result", float(one) + float(two))
