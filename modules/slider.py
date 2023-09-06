import tkinter as tk
from tkinter import ttk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)

        # init input, output
        self.input_init("fesz_p", "fesz_n", "fesz_l")
        self.output_init("scale_value", "scale_value2")

        # init own widget
        self.sc = ttk.Scale(self.wiget_parent_get(), from_=0, to=100, orient='horizontal', command=lambda value: self.output_set(value))
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        # position widgets
        self.sc.pack(fill=tk.X, side="bottom", expand=True)


        # set input, output init values
        self.input_value_set("fesz_p", 134)
        self.input_value_set("fesz_n", 1.34)

        self.output_set(self.sc.get())


    def output_set(self, value):
        self.output_value_set("scale_value", int(float(value)))
        self.output_value_set("scale_value2", int(float(value) * float(value)))
