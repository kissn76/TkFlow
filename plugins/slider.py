import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pluginbase



class Plugin(pluginbase.Pluginbase):
    def __init__(self, plugin_id, plugincontainer_object, canvas_object, **kwargs):
        super().__init__(plugin_id, plugincontainer_object, canvas_object, **kwargs)

        self.sc = None
        self.marker_widget = None
        self.content_frame = None

        # init input, output
        self.output_init("value")

        # init own plugin
        self.content_set()

        # set input, output init values
        self.output_value_set("value", self.sc.get())


    def content_set(self):
        self.content_frame = ttk.Frame(self.view_get())

        self.marker_widget = ttk.Label(self.content_frame, text=f"{self.view_get().plugincontainer.id_get()}-{self.id_get()}")
        self.sc = ttk.Scale(self.content_frame, from_=-100, to=100, orient='horizontal', command=lambda _: self.run())

        self.marker_widget.pack(anchor="nw", fill=tk.BOTH)
        self.sc.pack(anchor="nw", fill=tk.BOTH)

        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.view_init()
        self.content_init(self.content_frame)


    def run(self):
        self.output_value_set("value", int(self.sc.get()))


    # def settings(self, event):
    #     print("overwrited")
