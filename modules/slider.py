import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import widgetbase



class Plugin(widgetbase.WidgetBase):
    def __init__(self, master):
        super().__init__(master)
        MAX_SIZE = (24, 24)
        image_setting = Image.open(f"./resources/icon/setting.png")
        image_setting.thumbnail(MAX_SIZE)
        self.img_setting = ImageTk.PhotoImage(image_setting)

        # init input, output
        self.output_init("value")

        # init own widget
        self.sc = ttk.Scale(self, from_=0, to=100, orient='horizontal', command=lambda _: self.run())
        self.sc.bind("<Button-4>", lambda _: self.sc.set(self.sc.get() + 1))
        self.sc.bind("<Button-5>", lambda _: self.sc.set(self.sc.get() - 1))

        # position widgets
        self.sc.grid(row=0, column=1, sticky="we")
        self.sc.bind('<Button-3>', self.settings)

        # set input, output init values
        self.output_value_set("value", self.sc.get())


    def run(self):
        self.output_value_set("value", int(self.sc.get()))
