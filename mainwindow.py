import cv2
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import maincanvas


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New project", command=None)
        filemenu.add_command(label="Open project", command=None)
        filemenu.add_command(label="Save project", command=None)
        filemenu.add_command(label="Save project as...", command=None)
        filemenu.add_command(label="Close project", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.config(menu=menubar)

        self.frm_main = ttk.Frame(self)
        self.can_main = tk.Canvas(self.frm_main, scrollregion=(0, 0, 2000, 2000))
        hbar=ttk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky="e, w")
        hbar.config(command=self.can_main.xview)
        vbar=ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky="n, s")
        vbar.config(command=self.can_main.yview)
        self.can_main.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.can_main.grid(row=0, column=0, sticky="n, s, w, e")
        self.can_main.rowconfigure(0, weight=1)
        self.can_main.columnconfigure(0, weight=1)
        self.can_main.bind('<Button-1>', self.widget_dnd_select)

        self.frm_sidebar = ttk.Frame(self)
        self.frm_available_commands = ttk.LabelFrame(self.frm_sidebar, text="Available commands")
        self.frm_available_commands.grid(row=0, column=0)

        self.frm_sidebar.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_main.grid(row=0, column=1, sticky="n, s, w, e")
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


        self.widget_create()


    def widget_create(self, x=100, y=100):
        self.image_move = ImageTk.PhotoImage(Image.open("move.png"))
        id_move = self.can_main.create_image(x, y, image=self.image_move, anchor="nw")
        self.can_main.addtag_withtag("move", id_move)

        id_command = self.can_main.create_text(x + 24, y, text="Widget", anchor="nw")
        self.can_main.addtag_withtag("command", id_command)

        dv = ttk.Scale(self.can_main, from_=0, to=100, orient='horizontal')
        id_display_widget = self.can_main.create_window(x, y + 24, window=dv, anchor="nw")
        self.can_main.addtag_withtag("display_widget", id_display_widget)

        id_background = self.can_main.create_rectangle(x, y, x + 100, y + 100, fill='red', outline='red')
        self.can_main.addtag_withtag("background", id_background)
        self.can_main.tag_lower(id_background, id_move)


    # DRAG & DROP metódusok
    def widget_dnd_select(self, move):
        self.can_main.bind('<Motion>', self.widget_dnd_move)
        self.can_main.bind('<ButtonRelease-1>', self.widget_dnd_deselect)
        self.can_main.addtag_withtag('selected', tk.CURRENT)


    def widget_dnd_move(self, event):
        self.widget_move(event.x, event.y)


    def widget_dnd_deselect(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')


    def widget_move(self, x, y):
        canvas_x = self.can_main.canvasx(x)
        canvas_y = self.can_main.canvasy(y)
        if x > self.can_main.winfo_width():
            self.can_main.xview_scroll(1, 'units')
        if x < 1:
            self.can_main.xview_scroll(-1, 'units')
        if y > self.winfo_height():
            self.can_main.yview_scroll(1, 'units')
        if y < 1:
            self.can_main.yview_scroll(-1, 'units')

        self.can_main.coords("move", canvas_x, canvas_y)
        self.can_main.coords("command", canvas_x + 16, canvas_y)
        self.can_main.coords("display_widget", canvas_x, canvas_y + 16)
        self.can_main.coords("background", canvas_x, canvas_y, canvas_x + 100, canvas_y + 100)

        # if bool(move_box):
        #     move_x0, move_y0, move_x1, move_y1 = move_box
        #     self.coords(f"{command_name}.settings", move_x0, move_y1 + self.padding)
        #     settings_x0, settings_y0, settings_x1, settings_y1 = self.bbox(f"{command_name}.settings")
        #     self.coords(f"{command_name}.delete", settings_x0, settings_y1 + self.padding)
        #     delete_x0, delete_y0, delete_x1_, delete_y1 = self.bbox(f"{command_name}.delete")

        #     command_y0 = move_y0 - self.padding
        #     background_x1 = move_x1
        #     before_input_x0 = move_x1
        #     for input_key in command_obj.command_model.input.keys():
        #         command_y0 = move_y1
        #         self.coords(f"{command_name}.{input_key}", before_input_x0 + self.padding, move_y0)
        #         _, _, before_input_x0, _ = self.bbox(f"{command_name}.{input_key}")

        #         if background_x1 < before_input_x0:
        #             background_x1 = before_input_x0

        #     self.coords(f"{command_name}.command", move_x1 + self.padding, command_y0 + self.padding)
        #     name_x0, _, name_x1, name_y1 = self.bbox(f"{command_name}.command")

        #     self.coords(f"{command_name}.display_widget", move_x1 + self.padding, name_y1 + self.padding)

        #     if background_x1 < name_x1:
        #         background_x1 = name_x1

        #     background_y1 = delete_y1
        #     before_output_x0 = move_x1
        #     for output_name in command_obj.command_model.output.values():
        #         self.coords(output_name, before_output_x0 + self.padding, name_y1 + self.padding)
        #         output_x0, output_y0, before_output_x0, output_y1 = self.bbox(output_name)
        #         self.coords(f"{output_name}.clipboard", output_x0, output_y0, before_output_x0, output_y1)
        #         self.coords(f"{output_name}.preview", output_x0 - 2, output_y0 - 2, before_output_x0 + 2, output_y1 + 2)

        #         if background_y1 < output_y1:
        #             background_y1 = output_y1
        #         if background_x1 < before_output_x0:
        #             background_x1 = before_output_x0

        #     self.coords(f"{command_name}.background", move_x0 - self.padding, move_y0 - self.padding, background_x1 + self.padding, background_y1 + self.padding)

        #     self.io_widgets_connect(command_name)
    # DRAG & DROP metódusok END


    def quit(self):
        super().quit()
