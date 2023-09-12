import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import plugincontroller



can_main = None


class Mainwindow(tk.Tk):
    def __init__(self):
        global can_main
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.geometry("1200x400")

        # widget settings
        self.widget_width_min = 200
        self.widget_height_min = 0
        self.widget_resizer_width = 3
        self.widget_padding = 6
        # widget settings end

        self.widget_container = {}  # It contains all widget {widget_id: widget_object}
        self.plugin_container = {}  # It contains all used plugin {plugin_id: plugin_object}
        self.widget_counter = 0
        self.plugin_counter = 0

        self.image_move = ImageTk.PhotoImage(Image.open(f"./resources/icon/move.png"))

        self.plugin = plugincontroller.Plugincontroller()

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
        can_main = tk.Canvas(self.frm_main, scrollregion=(0, 0, 2000, 2000))
        hbar=ttk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky="e, w")
        hbar.config(command=can_main.xview)
        vbar=ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky="n, s")
        vbar.config(command=can_main.yview)
        can_main.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        can_main.grid(row=0, column=0, sticky="n, s, w, e")
        can_main.rowconfigure(0, weight=1)
        can_main.columnconfigure(0, weight=1)
        can_main.bind('<Button-1>', self.widget_dnd_select)

        self.frm_sidebar = ttk.Frame(self)
        self.frm_available_plugins = ttk.LabelFrame(self.frm_sidebar, text="Available plugins")
        self.frm_available_plugins.grid(row=0, column=0)

        self.frm_main.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_sidebar.grid(row=0, column=1, sticky="n, s, w, e")
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.floating_widget = None

        self.plugins_load()

        self.after(0, self.run)


    def run(self):
        for plugin_name, plugin_object in self.plugin_container.items():
            plugin_object.run()

        self.after(100, self.run)


    # loop through available plugins
    def plugins_load(self):
        # add available plugin to gui
        def available_plugin_add(plugin):
            w = ttk.Label(self.frm_available_plugins, text=plugin)
            w.pack(anchor="nw", fill=tk.BOTH)
            w.bind('<Button-1>', lambda event: self.plugin_dnd_start(event, plugin))
            w.bind('<B1-Motion>', lambda event: self.plugin_dnd_motion(event))
            w.bind('<ButtonRelease-1>', lambda event: self.plugin_dnd_stop(event, plugin))

        for m in self.plugin.list_plugins():
            available_plugin_add(plugin=m)


    # insert plugin to an existing widget
    def widget_plugin_insert(self, widget_id, plugin):
        plugin_id = f"{widget_id}:{plugin}.{self.plugin_counter}"
        plugin_container = self.widget_container[widget_id]
        plugin = self.plugin.new_object(plugin, master=plugin_container, id=plugin_id)
        plugin.pack(anchor="nw", fill=tk.BOTH)
        self.plugin_container.update({plugin_id: plugin})
        self.plugin_counter += 1

        return plugin_id


    # create new widget
    def widget_create(self, plugin, x=24, y=24):
        widget_id = f"widget.{self.widget_counter}"

        # mover
        can_main.create_image(x, y, image=self.image_move, anchor="nw", tags=[f"{widget_id}:move"])
        can_main.tag_bind(f"{widget_id}:move", "<Enter>", lambda event: can_main.config(cursor="hand1"))
        can_main.tag_bind(f"{widget_id}:move", "<Leave>", lambda event: can_main.config(cursor=""))

        # name
        can_main.create_text(0, 0, text=widget_id, anchor="nw", tags=[f"{widget_id}:name"])

        # plugin container add
        plugin_container = ttk.Frame(can_main)
        self.widget_container.update({widget_id: plugin_container})
        plugin_id = self.widget_plugin_insert(widget_id, plugin)
        can_main.create_window(0, 0, window=plugin_container, anchor="nw", width=self.widget_width_min - self.widget_padding * 2, tags=f"{widget_id}:plugincontainer")

        # background
        can_main.create_rectangle(0, 0, 0, 0, fill='red', outline='red', tags=[f"{widget_id}:background"])
        can_main.tag_lower(f"{widget_id}:background", f"{widget_id}:move")

        # resizer
        can_main.create_line(0, 0, 0, 0, width=self.widget_resizer_width, tags=[f"{widget_id}:resize_w"])
        can_main.tag_bind(f"{widget_id}:resize_w", "<Enter>", lambda event: can_main.config(cursor="right_side"))
        can_main.tag_bind(f"{widget_id}:resize_w", "<Leave>", lambda event: can_main.config(cursor=""))
        can_main.tag_bind(f"{widget_id}:resize_w", "<Double-Button-1>", lambda event: self.widget_resize_width(widget_id, 0))

        can_main.create_line(0, 0, 0, 0, width=self.widget_resizer_width, tags=[f"{widget_id}:resize_h"])
        can_main.tag_bind(f"{widget_id}:resize_h", "<Enter>", lambda event: can_main.config(cursor="bottom_side"))
        can_main.tag_bind(f"{widget_id}:resize_h", "<Leave>", lambda event: can_main.config(cursor=""))
        can_main.tag_bind(f"{widget_id}:resize_h", "<Double-Button-1>", lambda event: self.widget_resize_height(widget_id, 0))

        can_main.create_rectangle(0, 0, 0, 0, fill='black', outline='yellow', tags=[f"{widget_id}:resize_wh"])
        can_main.tag_bind(f"{widget_id}:resize_wh", "<Enter>", lambda event: can_main.config(cursor="bottom_right_corner"))
        can_main.tag_bind(f"{widget_id}:resize_wh", "<Leave>", lambda event: can_main.config(cursor=""))
        can_main.tag_bind(f"{widget_id}:resize_wh", "<Double-Button-1>", lambda event: self.widget_resize(widget_id, 0, 0))

        # set position and size of widget's parts
        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id)
        self.widget_resizer_set(widget_id)

        self.widget_counter += 1


    # set position and size of widget name
    def widget_name_set(self, widget_id):
        move_box = can_main.bbox(f"{widget_id}:move")
        can_main.coords(f"{widget_id}:name", move_box[2] + self.widget_padding, move_box[1])


    # set position and size of plugin container
    def widget_plugin_container_set(self, widget_id):
        move_box = can_main.bbox(f"{widget_id}:move")
        can_main.coords(f"{widget_id}:plugincontainer", move_box[0], move_box[3] + self.widget_padding)


    # set position and size of background
    def widget_background_set(self, widget_id, move=False, right_side=None, bottom_side=None):
        move_box = can_main.bbox(f"{widget_id}:move")
        background_box = can_main.bbox(f"{widget_id}:background")

        background_box_width = background_box[2] - background_box[0] - 2
        background_box_height = background_box[3] - background_box[1] - 2

        if not bool(move):
            plugin_container_box = can_main.bbox(f"{widget_id}:plugincontainer")

            if not right_side is None:
                background_box_width = right_side - background_box[0]

            if not bottom_side is None:
                background_box_height = bottom_side - background_box[1]

            if background_box_width < self.widget_width_min:
                background_box_width = self.widget_width_min

            if background_box_height < self.widget_height_min:
                background_box_height = self.widget_height_min
            if background_box_height < plugin_container_box[3] - move_box[1] - 2 + self.widget_padding * 2:
                background_box_height = plugin_container_box[3] - move_box[1] - 2 + self.widget_padding * 2

        can_main.coords(
                f"{widget_id}:background",
                move_box[0] - self.widget_padding, move_box[1] - self.widget_padding,
                move_box[0] - self.widget_padding + background_box_width, move_box[1] - self.widget_padding + background_box_height,
            )

        return background_box_width, background_box_height


    # set position and size of resizer lines
    def widget_resizer_set(self, widget_id):
        background_box = can_main.bbox(f"{widget_id}:background")

        # width resizer line
        can_main.coords(
                f"{widget_id}:resize_w",
                background_box[2], background_box[1] + 1,
                background_box[2], background_box[3]
            )

        # height resizer line
        can_main.coords(
                f"{widget_id}:resize_h",
                background_box[0] + 1, background_box[3],
                background_box[2], background_box[3]
            )

        # width & height resizer rectangle
        can_main.coords(
                f"{widget_id}:resize_wh",
                background_box[2] - self.widget_resizer_width, background_box[3] - self.widget_resizer_width,
                background_box[2] + self.widget_resizer_width, background_box[3] + self.widget_resizer_width
            )

# DRAG & DROP metódusok
    # plugin list methods
    def plugin_dnd_start(self, event, text):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

        self.floating_widget = ttk.Label(self, text=text)
        self.floating_widget.place(x=x, y=y)


    def plugin_dnd_motion(self, event):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        canvas_x = can_main.canvasx(x)
        canvas_y = can_main.canvasy(y)

        self.floating_widget.place(x=x, y=y)

        can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, can_main.cget("scrollregion").split()))

        if canvas_x <= 0 or canvas_y <= 0 or canvas_x >= can_main_width - self.widget_padding * 2 or canvas_y >= can_main_height - self.widget_padding * 2:
            self.config(cursor="X_cursor")
        else:
            self.config(cursor="")


    def plugin_dnd_stop(self, event, plugin):
        self.config(cursor="")
        self.floating_widget.place_forget()
        self.floating_widget.destroy()

        if event.x < 0:
            x = self.winfo_pointerx() - self.winfo_rootx()
            y = self.winfo_pointery() - self.winfo_rooty()
            canvas_x = can_main.canvasx(x)
            canvas_y = can_main.canvasy(y)

            can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, can_main.cget("scrollregion").split()))
            if canvas_x > 0 and canvas_y > 0 and canvas_x < can_main_width - self.widget_padding * 2 and canvas_y < can_main_height - self.widget_padding * 2:
                try:
                    widgets = can_main.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)

                    if len(widgets) == 0:
                        self.widget_create(plugin=plugin, x=canvas_x, y=canvas_y)
                    else:
                        widget_ids = set()
                        for id in widgets:
                            tags = can_main.gettags(id)
                            if len(tags) > 0:
                                widget_id, _ = tags[0].split(':')
                                widget_ids.add(widget_id)

                        if len(widget_ids) == 1:
                            target_widget_id = list(widget_ids)[0]
                            self.widget_plugin_insert(target_widget_id, plugin)
                        else:
                            print("too many widget are overlapped:", widget_ids)
                except:
                    pass

    # widget methods
    def widget_dnd_select(self, move):
        can_main.bind('<Motion>', self.widget_dnd_move)
        can_main.bind('<ButtonRelease-1>', self.widget_dnd_deselect)
        can_main.addtag_withtag('selected', tk.CURRENT)


    def widget_dnd_move(self, event):
        tags = can_main.gettags('selected')
        if len(tags) > 0:
            widget_id, widget_function = tags[0].split(':')
            mouse_x, mouse_y = event.x, event.y
            if widget_function == "move":
                self.widget_move(widget_id, mouse_x, mouse_y)
            elif widget_function == "resize_w":
                self.widget_resize_width(widget_id, mouse_x)
            elif widget_function == "resize_h":
                self.widget_resize_height(widget_id, mouse_y)
            elif widget_function == "resize_wh":
                self.widget_resize(widget_id, mouse_x, mouse_y)


    def widget_dnd_deselect(self, event):
        can_main.dtag('selected')    # removes the 'selected' tag
        can_main.unbind('<Motion>')

# DRAG & DROP metódusok END


    def widget_resize(self, widget_id, x, y):
        self.widget_resize_width(widget_id, x)
        self.widget_resize_height(widget_id, y)


    def widget_resize_width(self, widget_id, x):
        canvas_x = can_main.canvasx(x)
        if x > can_main.winfo_width():
            can_main.xview_scroll(1, 'units')
        if x < 1:
            can_main.xview_scroll(-1, 'units')

        bg_w, _ = self.widget_background_set(widget_id, right_side=canvas_x)

        can_main.itemconfigure(f"{widget_id}:plugincontainer", width=bg_w - self.widget_padding * 2)

        self.widget_resizer_set(widget_id)

        for plugin_key, plugin_object in self.plugin_container.items():
            if plugin_key.startswith(widget_id):
                plugin_object.connect()


    def widget_resize_height(self, widget_id, y):
        canvas_y = can_main.canvasy(y)
        if y > self.winfo_height():
            can_main.yview_scroll(1, 'units')
        if y < 1:
            can_main.yview_scroll(-1, 'units')

        self.widget_background_set(widget_id, bottom_side=canvas_y)

        self.widget_resizer_set(widget_id)


    def widget_move(self, widget_id, x, y):
        canvas_x = can_main.canvasx(x)
        canvas_y = can_main.canvasy(y)
        if x > can_main.winfo_width():
            can_main.xview_scroll(1, 'units')
        if x < 1:
            can_main.xview_scroll(-1, 'units')
        if y > self.winfo_height():
            can_main.yview_scroll(1, 'units')
        if y < 1:
            can_main.yview_scroll(-1, 'units')

        can_main.coords(f"{widget_id}:move", canvas_x, canvas_y)

        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id, move=True)
        self.widget_resizer_set(widget_id)

        for plugin_key, plugin_object in self.plugin_container.items():
            if plugin_key.startswith(widget_id):
                plugin_object.connect()


    def quit(self):
        super().quit()
