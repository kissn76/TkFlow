import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, plugin_id, pluginframe_object, canvas_object, **kwargs):
        super().__init__(plugin_id, pluginframe_object, canvas_object, **kwargs)

        self.show = None

        # init input, output
        self.inputvariable_init("in")

        # init own plugin
        self.content_set(pluginframe_object)


    def content_set(self, pluginframe_object):
        self.view_create(pluginframe_object)
        self.view_init()

        self.show = ttk.Label(self.view_get(), text="")

        self.contentrow_init(self.show)


    def run(self):
        inp = self.input_value_get("in")

        if not bool(inp):
            inp = 0

        self.show.configure(text=str(inp))
