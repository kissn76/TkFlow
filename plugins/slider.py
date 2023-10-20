import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, plugin_id, plugincontainer_object, canvas_object, **kwargs):
        super().__init__(plugin_id, plugincontainer_object, canvas_object, **kwargs)

        self.sc = None

        # init input, output
        self.output_init("value")

        # init own plugin
        self.content_set()

        # set input, output init values
        self.output_value_set("value", self.sc.get())


    def content_destroy(self):
        if bool(self.sc):
            self.sc.grid_forget()
            self.sc.destroy()
            self.sc = None


    def content_set(self):
        self.sc = ttk.Scale(self.view_get(), from_=-100, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.view_init()
        self.content_init(self.sc)



    def run(self):
        self.output_value_set("value", int(self.sc.get()))


    # def settings(self, event):
    #     print("overwrited")
