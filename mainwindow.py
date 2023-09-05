import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import module
import widgetbase


class Mainwindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.geometry("1200x400")

        # widget settings
        self.widget_width_min = 200
        self.widget_height_min = 0
        self.widget_resizer_width = 3
        self.widget_padding = 6
        # widget settings end

        self.widget_counter = 0

        self.image_move = ImageTk.PhotoImage(Image.open(f"./resources/icon/move.png"))

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
        # w.bind('<Double-Button-1>', lambda event: self.widget_create(module, 24, 24))
        w.bind('<Button-1>', lambda event: self.widget_dnd_start(event))
        w.bind('<ButtonRelease-1>', lambda event: self.widget_dnd_stop(event, module))


    def check_hand_enter(self, cursor="hand1"):
        self.can_main.config(cursor=cursor)


    def check_hand_leave(self):
        self.can_main.config(cursor="")


    def widget_create(self, module, x=24, y=24):
        widget_name = f"widget.{self.widget_counter}"
        module_name = f"{module}.{self.widget_counter}"

        # mover
        self.can_main.create_image(x, y, image=self.image_move, anchor="nw", tags=[f"{widget_name}.move"])
        self.can_main.tag_bind(f"{widget_name}.move", "<Enter>", lambda event: self.check_hand_enter(cursor="hand1"))
        self.can_main.tag_bind(f"{widget_name}.move", "<Leave>", lambda event: self.check_hand_leave())

        # name
        self.can_main.create_text(0, 0, text=widget_name, anchor="nw", tags=[f"{widget_name}.widget_name"])
        self.widget_name_set(widget_name)

        # module add
        module = self.modules.new_object(module, master=self.can_main)
        self.can_main.create_window(0, 0, window=module, anchor="nw", width=self.widget_width_min - self.widget_padding * 2, tags=[f"{widget_name}.module", f"{module_name}.module"])
        self.widget_module_set(widget_name)

        # background
        self.can_main.create_rectangle(0, 0, 0, 0, fill='red', outline='red', tags=[f"{widget_name}.background"])
        self.widget_background_set(widget_name)
        self.can_main.tag_lower(f"{widget_name}.background", f"{widget_name}.move")

        # resizer
        self.can_main.create_line(0, 0, 0, 0, width=self.widget_resizer_width, tags=[f"{widget_name}.resize_w"])
        self.can_main.tag_bind(f"{widget_name}.resize_w", "<Enter>", lambda event: self.check_hand_enter(cursor="right_side"))
        self.can_main.tag_bind(f"{widget_name}.resize_w", "<Leave>", lambda event: self.check_hand_leave())
        self.can_main.tag_bind(f"{widget_name}.resize_w", "<Double-Button-1>", lambda event: self.widget_resize_width(widget_name, 0))

        self.can_main.create_line(0, 0, 0, 0, width=self.widget_resizer_width, tags=[f"{widget_name}.resize_h"])
        self.can_main.tag_bind(f"{widget_name}.resize_h", "<Enter>", lambda event: self.check_hand_enter(cursor="bottom_side"))
        self.can_main.tag_bind(f"{widget_name}.resize_h", "<Leave>", lambda event: self.check_hand_leave())
        self.can_main.tag_bind(f"{widget_name}.resize_h", "<Double-Button-1>", lambda event: self.widget_resize_height(widget_name, 0))

        self.can_main.create_rectangle(0, 0, 0, 0, fill='black', outline='yellow', tags=[f"{widget_name}.resize_wh"])
        self.can_main.tag_bind(f"{widget_name}.resize_wh", "<Enter>", lambda event: self.check_hand_enter(cursor="bottom_right_corner"))
        self.can_main.tag_bind(f"{widget_name}.resize_wh", "<Leave>", lambda event: self.check_hand_leave())
        self.can_main.tag_bind(f"{widget_name}.resize_wh", "<Double-Button-1>", lambda event: self.widget_resize(widget_name, 0, 0))

        self.widget_resizer_set(widget_name)

        self.widget_counter += 1


    def widget_name_set(self, widget_name):
        move_box = self.can_main.bbox(f"{widget_name}.move")
        self.can_main.coords(f"{widget_name}.widget_name", move_box[2] + self.widget_padding, move_box[1])


    def widget_module_set(self, widget_name):
        move_box = self.can_main.bbox(f"{widget_name}.move")
        self.can_main.coords(f"{widget_name}.module", move_box[0], move_box[3] + self.widget_padding)


    def widget_background_set(self, widget_name, move=False, right_side=None, bottom_side=None):
        move_box = self.can_main.bbox(f"{widget_name}.move")
        background_box = self.can_main.bbox(f"{widget_name}.background")

        background_box_width = background_box[2] - background_box[0] - 2
        background_box_height = background_box[3] - background_box[1] - 2

        if not bool(move):
            module_box = self.can_main.bbox(f"{widget_name}.module")

            if not right_side is None:
                background_box_width = right_side - background_box[0]

            if not bottom_side is None:
                background_box_height = bottom_side - background_box[1]

            if background_box_width < self.widget_width_min:
                background_box_width = self.widget_width_min

            if background_box_height < self.widget_height_min:
                background_box_height = self.widget_height_min
            if background_box_height < module_box[3] - move_box[1] - 2 + self.widget_padding * 2:
                background_box_height = module_box[3] - move_box[1] - 2 + self.widget_padding * 2

        self.can_main.coords(
                f"{widget_name}.background",
                move_box[0] - self.widget_padding, move_box[1] - self.widget_padding,
                move_box[0] - self.widget_padding + background_box_width, move_box[1] - self.widget_padding + background_box_height,
            )

        return background_box_width, background_box_height


    def widget_resizer_set(self, widget_name):
        background_box = self.can_main.bbox(f"{widget_name}.background")

        # width resizer line
        self.can_main.coords(
                f"{widget_name}.resize_w",
                background_box[2], background_box[1] + 1,
                background_box[2], background_box[3]
            )

        # height resizer line
        self.can_main.coords(
                f"{widget_name}.resize_h",
                background_box[0] + 1, background_box[3],
                background_box[2], background_box[3]
            )

        # width & height resizer rectangle
        self.can_main.coords(
                f"{widget_name}.resize_wh",
                background_box[2] - self.widget_resizer_width, background_box[3] - self.widget_resizer_width,
                background_box[2] + self.widget_resizer_width, background_box[3] + self.widget_resizer_width
            )

    # DRAG & DROP metódusok

    def widget_dnd_start(self, event):
        pass
        # print(event.x, event.x_root, self.can_main.canvasx(event.x_root))


    def widget_dnd_stop(self, event, module):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        canvas_x = self.can_main.canvasx(x)
        canvas_y = self.can_main.canvasy(y)

        try:
            widgets = self.can_main.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)

            if len(widgets) == 0:
                self.widget_create(module=module, x=canvas_x, y=canvas_y)
            else:
                widget_ids = set()
                for id in widgets:
                    tags = self.can_main.gettags(id)
                    if len(tags) > 0:
                        _, widget_counter, widget_function = tags[0].split('.')
                        widget_ids.add(widget_counter)

                if len(widget_ids) == 1:
                    print(f"adding module to widget.{list(widget_ids)[0]}")
                else:
                    print("too many widget are overlapped:", widget_ids)
        except:
            pass


    def widget_dnd_select(self, move):
        self.can_main.bind('<Motion>', self.widget_dnd_move)
        self.can_main.bind('<ButtonRelease-1>', self.widget_dnd_deselect)
        self.can_main.addtag_withtag('selected', tk.CURRENT)


    def widget_dnd_move(self, event):
        tags = self.can_main.gettags('selected')
        if len(tags) > 0:
            _, widget_counter, widget_function = tags[0].split('.')
            widget_name = f"widget.{widget_counter}"
            mouse_x, mouse_y = event.x, event.y
            if widget_function == "move":
                self.widget_move(widget_name, mouse_x, mouse_y)
            elif widget_function == "resize_w":
                self.widget_resize_width(widget_name, mouse_x)
            elif widget_function == "resize_h":
                self.widget_resize_height(widget_name, mouse_y)
            elif widget_function == "resize_wh":
                self.widget_resize(widget_name, mouse_x, mouse_y)


    def widget_dnd_deselect(self, event):
        self.can_main.dtag('selected')    # removes the 'selected' tag
        self.can_main.unbind('<Motion>')


    def widget_resize(self, widget_name, x, y):
        self.widget_resize_width(widget_name, x)
        self.widget_resize_height(widget_name, y)


    def widget_resize_width(self, widget_name, x):
        canvas_x = self.can_main.canvasx(x)
        if x > self.can_main.winfo_width():
            self.can_main.xview_scroll(1, 'units')
        if x < 1:
            self.can_main.xview_scroll(-1, 'units')

        bg_w, _ = self.widget_background_set(widget_name, right_side=canvas_x)

        self.can_main.itemconfigure(f"{widget_name}.module", width=bg_w - self.widget_padding * 2)

        self.widget_resizer_set(widget_name)


    def widget_resize_height(self, widget_name, y):
        canvas_y = self.can_main.canvasy(y)
        if y > self.winfo_height():
            self.can_main.yview_scroll(1, 'units')
        if y < 1:
            self.can_main.yview_scroll(-1, 'units')

        self.widget_background_set(widget_name, bottom_side=canvas_y)

        self.widget_resizer_set(widget_name)


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

        self.widget_name_set(widget_name)
        self.widget_module_set(widget_name)
        self.widget_background_set(widget_name, move=True)
        self.widget_resizer_set(widget_name)

    # DRAG & DROP metódusok END


    def quit(self):
        super().quit()
