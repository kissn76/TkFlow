import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginbase



class Plugin(pluginbase.PluginBase):
    def __init__(self, master=None, id=None, **kwargs):
        super().__init__(master, id, name="Slider", parents=["Widgets"], **kwargs)
        # init input, output
        self.output_init("value")

        # init own plugin
        self.sc = ttk.Scale(self, from_=-100, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        # position plugin
        self.sc.grid(row=0, column=1, sticky="we")

        # set input, output init values
        self.output_value_set("value", self.sc.get())


    def run(self):
        self.output_value_set("value", int(self.sc.get()))


    def settings(self, event):
        print("overwrited")
