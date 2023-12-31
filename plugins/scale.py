import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        # init input, output, setting variables
        self.outputvariable_init("value")
        self.settingvariable_init("from", -100)
        self.settingvariable_init("to", 100)

        # init settings view
        self.settingsview_get().savebtn_configure(self.content_set)
        self.settingrow_init("entry", "from", "From")
        self.settingrow_init("entry", "to", "To")

        # init own plugin view
        self.sc = ttk.Scale(self, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))
        self.contentrow_init(self.sc)
        self.content_set()

        # set input, output init values
        self.outputvariable_set("value", self.sc.get())


    def content_set(self):
        self.setting_save()

        if not self.settingvariable_get("from") == None:
            self.sc.configure(from_=self.settingvariable_get("from"))
        if not self.settingvariable_get("to") == None:
            self.sc.configure(to=self.settingvariable_get("to"))
        if not self.outputvariable_get("value") == None:
            self.sc.set(self.outputvariable_get("value"))


    def run(self):
        self.outputvariable_set("value", int(self.sc.get()))
