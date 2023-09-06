import tkinter as tk
from tkinter import ttk


class Plugin(ttk.Frame):
    def __init__(self, **kwargs):
        super(Plugin, self).__init__(**kwargs)
        lb_1 = ttk.Label(self, text="input")
        sc = ttk.Scale(self, from_=0, to=100, orient='horizontal', command=lambda value: lb_2.configure(text=int(float(value))))
        lb_2 = ttk.Label(self, text="output")

        lb_1.grid(row=0, column=0, sticky="n, s, w, e")
        sc.grid(row=0, column=1, sticky="n, s, w, e")
        lb_2.grid(row=0, column=2, sticky="n, s, w, e")

        self.columnconfigure(1, weight=1)

        sc.bind("<Button-4>", lambda _: sc.set(sc.get() + 1))
        sc.bind("<Button-5>", lambda _: sc.set(sc.get() - 1))
