import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        self.sc = None

        # init input, output, setting
        self.output_init("value")

        self.setting_init("from")
        self.setting_init("to")
        self.setting_value_set("from", -100)
        self.setting_value_set("to", 100)
        self.setting_value_set("value", 0)

        # init own plugin
        self.content_set()

        # set input, output init values
        self.output_value_set("value", self.sc.get())

        self.settings_set()


    def content_set(self):
        self.sc = ttk.Scale(self, from_=self.setting_value_get("from"), to=self.setting_value_get("to"), value=self.setting_value_get("value"), orient='horizontal', command=lambda _: self.run())

        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.content_init(self.sc)

        if bool(self.output_value_get("value")):
            self.sc.set(self.output_value_get("value"))


    def settings_set(self):
        entry_from = ttk.Entry(self.settings_viewframe_get())
        entry_to = ttk.Entry(self.settings_viewframe_get())
        entry_value = ttk.Entry(self.settings_viewframe_get())

        entry_from.insert(0, self.setting_value_get("from"))
        entry_to.insert(0, self.setting_value_get("to"))
        entry_value.insert(0, self.setting_value_get("value"))

        self.settings_content_init("From", entry_from)
        self.settings_content_init("To", entry_to)
        self.settings_content_init("Value", entry_value)


    def run(self):
        self.output_value_set("value", int(self.sc.get()))
