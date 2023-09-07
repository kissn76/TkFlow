import tkinter as tk
from tkinter import ttk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, master):
        super().__init__(master)

        # init input, output
        self.output_init("value", "value2")

        # init own widget
        self.sc = ttk.Scale(self.wiget_parent_get(), from_=0, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        self.sc2 = ttk.Scale(self.wiget_parent_get(), from_=0, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc2.bind("<Button-4>", lambda _: self.sc2.set(self.sc2.get() + 1))
        self.sc2.bind("<Button-5>", lambda _: self.sc2.set(self.sc2.get() - 1))

        # position widgets
        self.sc.pack(fill=tk.X, expand=True)
        self.sc2.pack(fill=tk.X, expand=True)

        # set input, output init values
        self.output_value_set("value", self.sc.get())
        self.output_value_set("value2", self.sc2.get())


    def run(self):
        self.output_value_set("value", int(self.sc.get()))
        self.output_value_set("value2", int(self.sc2.get()))
