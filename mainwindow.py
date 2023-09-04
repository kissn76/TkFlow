import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import module
import widgetbase


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)

        self.widget_width_min = 200
        self.widget_height_min = 100
        self.resize_width = 6
        self.widget_counter = 0

        self.image_move = ImageTk.PhotoImage(Image.open(f"./move.png"))

        self.modules = module.Module()

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

        self.frm_main.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_sidebar.grid(row=0, column=1, sticky="n, s, w, e")
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.modules_load()


    def modules_load(self):
        for m in self.modules.list_modules():
            self.available_command_add(module=m)


    def available_command_add(self, module):
        w = ttk.Label(self.frm_available_commands, text=module)
        w.pack()
        w.bind('<Double-Button-1>', lambda event: self.widget_create(module, 10, 10))


    def widget_create(self, module, x=10, y=10):
        widget_name = f"{module}.{self.widget_counter}"

        id_move = self.can_main.create_image(x, y, image=self.image_move, anchor="nw")
        self.can_main.addtag_withtag(f"{widget_name}.move", id_move)
        move_box = self.can_main.bbox(f"{widget_name}.move")

        id_widget_name = self.can_main.create_text(move_box[2], move_box[1], text=widget_name, anchor="nw")
        self.can_main.addtag_withtag(f"{widget_name}.widget_name", id_widget_name)

        module = self.modules.new_object(module, self.can_main)
        id_module = self.can_main.create_window(move_box[0], move_box[3], window=module, anchor="nw", width=self.widget_width_min)
        self.can_main.addtag_withtag(f"{widget_name}.module", id_module)
        module_box = self.can_main.bbox(f"{widget_name}.module")

        background_box_width = module_box[2] - 1 - move_box[0] - 1
        background_box_height = module_box[3] - 1 - move_box[1] - 1
        if background_box_width < self.widget_width_min:
            background_box_width = self.widget_width_min
        if background_box_height < self.widget_height_min:
            background_box_height = self.widget_height_min
        id_background = self.can_main.create_rectangle(
                move_box[0],
                move_box[1],
                move_box[0] + background_box_width,
                move_box[1] + background_box_height,
                fill='red',
                outline='red'
            )
        self.can_main.addtag_withtag(f"{widget_name}.background", id_background)
        self.can_main.tag_lower(id_background, id_move)
        background_box = self.can_main.bbox(f"{widget_name}.background")

        id_resize_w = self.can_main.create_line(background_box[2], background_box[1] + 1, background_box[2], background_box[3], width=self.resize_width)
        self.can_main.addtag_withtag(f"{widget_name}.resize_w", id_resize_w)

        id_resize_h = self.can_main.create_line(background_box[0] + 1, background_box[3], background_box[2], background_box[3], width=self.resize_width)
        self.can_main.addtag_withtag(f"{widget_name}.resize_h", id_resize_h)

        id_resize_wh = self.can_main.create_rectangle(
                background_box[2] - self.resize_width,
                background_box[3] - self.resize_width,
                background_box[2] + self.resize_width,
                background_box[3] + self.resize_width,
                fill='black',
                outline='yellow'
            )
        self.can_main.addtag_withtag(f"{widget_name}.resize_wh", id_resize_wh)

        self.widget_counter += 1


    # DRAG & DROP metódusok
    def widget_dnd_select(self, move):
        self.can_main.bind('<Motion>', self.widget_dnd_move)
        self.can_main.bind('<ButtonRelease-1>', self.widget_dnd_deselect)
        self.can_main.addtag_withtag('selected', tk.CURRENT)


    def widget_dnd_move(self, event):
        tags = self.can_main.gettags('selected')
        if len(tags) > 0:
            module_name, module_counter, widget_function = tags[0].split('.')
            mouse_x, mouse_y = event.x, event.y
            if widget_function == "move":
                self.widget_move(f"{module_name}.{module_counter}", mouse_x, mouse_y)
            elif widget_function == "resize_w":
                self.widget_resize_width(f"{module_name}.{module_counter}", mouse_x)
            elif widget_function == "resize_h":
                self.widget_resize_height(f"{module_name}.{module_counter}", mouse_y)
            elif widget_function == "resize_wh":
                self.widget_resize_width(f"{module_name}.{module_counter}", mouse_x)
                self.widget_resize_height(f"{module_name}.{module_counter}", mouse_y)


    def widget_dnd_deselect(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')


    def widget_resize_width(self, widget_name, x):
        canvas_x = self.can_main.canvasx(x)
        if x > self.can_main.winfo_width():
            self.can_main.xview_scroll(1, 'units')
        if x < 1:
            self.can_main.xview_scroll(-1, 'units')

        move_box = self.can_main.bbox(f"{widget_name}.move")
        width = canvas_x - move_box[0]
        if width >= self.widget_width_min:
            background_box = self.can_main.bbox(f"{widget_name}.background")
            self.can_main.coords(f"{widget_name}.background", move_box[0], move_box[1], canvas_x, background_box[3] - 1)
            background_box = self.can_main.bbox(f"{widget_name}.background")
            self.can_main.itemconfigure(f"{widget_name}.module", width=width)
            self.can_main.coords(f"{widget_name}.resize_w", background_box[2], background_box[1] + 1, background_box[2], background_box[3])
            self.can_main.coords(f"{widget_name}.resize_h", background_box[0] + 1, background_box[3], background_box[2], background_box[3])
            self.can_main.coords(f"{widget_name}.resize_wh", background_box[2] - self.resize_width, background_box[3] - self.resize_width, background_box[2] + self.resize_width, background_box[3] + self.resize_width)


    def widget_resize_height(self, widget_name, y):
        canvas_y = self.can_main.canvasy(y)
        if y > self.winfo_height():
            self.can_main.yview_scroll(1, 'units')
        if y < 1:
            self.can_main.yview_scroll(-1, 'units')

        move_box = self.can_main.bbox(f"{widget_name}.move")
        height = canvas_y - move_box[1]
        if height >= self.widget_height_min:
            background_box = self.can_main.bbox(f"{widget_name}.background")
            self.can_main.coords(f"{widget_name}.background", move_box[0], move_box[1], background_box[2] - 1, canvas_y)
            background_box = self.can_main.bbox(f"{widget_name}.background")
            self.can_main.coords(f"{widget_name}.resize_w", background_box[2], background_box[1] + 1, background_box[2], background_box[3])
            self.can_main.coords(f"{widget_name}.resize_h", background_box[0] + 1, background_box[3], background_box[2], background_box[3])
            self.can_main.coords(f"{widget_name}.resize_wh", background_box[2] - self.resize_width, background_box[3] - self.resize_width, background_box[2] + self.resize_width, background_box[3] + self.resize_width)


    def widget_move(self, widget_name, x, y):
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

        self.can_main.coords(f"{widget_name}.move", canvas_x, canvas_y)
        move_box = self.can_main.bbox(f"{widget_name}.move")

        self.can_main.coords(f"{widget_name}.widget_name", move_box[2], move_box[1])
        self.can_main.coords(f"{widget_name}.module", move_box[0], move_box[3])

        background_box = self.can_main.bbox(f"{widget_name}.background")
        background_box_width = background_box[2] - 1 - background_box[0] - 1
        background_box_height = background_box[3] - 1 - background_box[1] - 1
        self.can_main.coords(
                f"{widget_name}.background",
                move_box[0],
                move_box[1],
                move_box[0] + background_box_width,
                move_box[1] + background_box_height
            )
        background_box = self.can_main.bbox(f"{widget_name}.background")

        self.can_main.coords(f"{widget_name}.resize_w", background_box[2], background_box[1] + 1, background_box[2], background_box[3])

        self.can_main.coords(f"{widget_name}.resize_h", background_box[0] + 1, background_box[3], background_box[2], background_box[3])

        self.can_main.coords(f"{widget_name}.resize_wh", background_box[2] - self.resize_width, background_box[3] - self.resize_width, background_box[2] + self.resize_width, background_box[3] + self.resize_width)
    # DRAG & DROP metódusok END


    def quit(self):
        super().quit()
