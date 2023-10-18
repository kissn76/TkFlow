import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, master, plugin_name, plugin_container_id, canvas_object, **kwargs):
        super().__init__(master, plugin_name, plugin_container_id, canvas_object, **kwargs)
        # init input, output
        self.output_init("value")

        # init own plugin
        self.sc = ttk.Scale(self.view_get(), from_=-100, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.content_init(self.sc)

        # set input, output init values
        self.output_value_set("value", self.sc.get())


    def run(self):
        self.output_value_set("value", int(self.sc.get()))


    # def settings(self, event):
    #     print("overwrited")
