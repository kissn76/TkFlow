import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, plugin_id, pluginframe_object, canvas_object, **kwargs):
        super().__init__(plugin_id, pluginframe_object, canvas_object, **kwargs)

        self.sc = None

        # init input, output, setting
        self.output_init("value")

        self.setting_init("from")
        self.setting_init("to")
        self.setting_value_set("from", -100)
        self.setting_value_set("to", 100)

        # init own plugin
        self.content_set(pluginframe_object)

        # set input, output init values
        self.output_value_set("value", self.sc.get())



    def content_set(self, pluginframe_object):
        self.view_create(pluginframe_object)
        self.view_init()

        self.sc = ttk.Scale(self.view_get(), from_=self.setting_value_get("from"), to=self.setting_value_get("to"), orient='horizontal', command=lambda _: self.run())

        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.content_init(self.sc)

        if bool(self.output_value_get("value")):
            self.sc.set(self.output_value_get("value"))


    def run(self):
        self.output_value_set("value", int(self.sc.get()))


    # def settings(self, event):
    #     print("overwrited")
