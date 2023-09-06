import tkinter as tk
from tkinter import ttk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, master):
        super().__init__(master)

        # init input, output
        self.output_init("value")

        # init own widget
        self.sc = ttk.Scale(self.wiget_parent_get(), from_=0, to=100, orient='horizontal', command=lambda value: self.output_set(value))
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        # position widgets
        self.sc.pack(fill=tk.BOTH)


        # set input, output init values
        self.output_set(self.sc.get())


    def output_set(self, value):
        self.output_value_set("value", int(float(value)))
