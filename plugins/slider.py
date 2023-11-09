import tkinter as tk
from tkinter import ttk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, pluginframe_object, canvas_object, model, **kwargs):
        super().__init__(pluginframe_object, canvas_object, model, **kwargs)

        self.sc = None

        # init input, output, setting
        self.outputvariable_init("value")

        self.settingvariable_init("from")
        self.settingvariable_init("to")
        self.settingvariable_set("from", -100)
        self.settingvariable_set("to", 100)
        self.settingvariable_set("value", 0)

        # init own plugin
        self.content_init()
        self.content_set()

        # set input, output init values
        self.outputvariable_set("value", self.sc.get())

        self.settings_init()


    def content_init(self):
        self.sc = ttk.Scale(self, orient='horizontal', command=lambda _: self.run())

        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.contentrow_init(self.sc)


    def content_set(self):
        self.settings_view.save()

        if not self.settingvariable_get("from") == None:
            self.sc.configure(from_=self.settingvariable_get("from"))
        if not self.settingvariable_get("to") == None:
            self.sc.configure(to=self.settingvariable_get("to"))
        if not self.outputvariable_get("value") == None:
            self.sc.set(self.outputvariable_get("value"))


    def settings_init(self):
        self.settings_view.savebtn_configure(self.content_set)

        self.settingrow_init("entry", "from", "From")
        self.settingrow_init("entry", "to", "To")


    def run(self):
        # print(self.sc.get())
        self.outputvariable_set("value", int(self.sc.get()))
