import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mainwindow
import plugincontainer
import style



class Maincanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.image_move = ImageTk.PhotoImage(style.image_move)


    # create new widget
    def widget_create(self, plugin_name, x=24, y=24):
        if x < style.widget_padding:
            x = style.widget_padding
        if y < style.widget_padding:
            y = style.widget_padding

        plugin_container = plugincontainer.Plugincontainer(self)
        widget_id = plugin_container.id

        # mover
        self.create_image(x, y, image=self.image_move, anchor="nw", tags=[f"{widget_id}:move"])
        self.tag_bind(f"{widget_id}:move", "<Enter>", lambda event: self.config(cursor="hand1"))
        self.tag_bind(f"{widget_id}:move", "<Leave>", lambda event: self.config(cursor=""))

        # name
        self.create_text(0, 0, text=widget_id, anchor="nw", tags=[f"{widget_id}:name"])

        # plugin container add
        self.create_window(
                0, 0,
                window=plugin_container,
                anchor="nw",
                width=style.widget_width_min - style.widget_padding * 2,
                tags=f"{widget_id}:plugincontainer"
            )
        plugin_container.plugin_insert(plugin_name)

        # background
        self.create_rectangle(0, 0, 0, 0, fill=style.widget_background_color, outline=style.widget_background_outline_color, tags=[f"{widget_id}:background"])
        self.tag_lower(f"{widget_id}:background", f"{widget_id}:move")

        # widget resizer
        print(style.widget_resizer_width)
        if style.widget_resizer_width > 0:
            # width resizer line
            if bool(style.widget_width_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_color, tags=[f"{widget_id}:resize_w"]
                )
                self.tag_bind(f"{widget_id}:resize_w", "<Enter>", lambda event: self.config(cursor="right_side"))
                self.tag_bind(f"{widget_id}:resize_w", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}:resize_w", "<Double-Button-1>", lambda event: self.widget_reset_width(widget_id))

            # height resizer line
            if bool(style.widget_height_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_color, tags=[f"{widget_id}:resize_h"]
                )
                self.tag_bind(f"{widget_id}:resize_h", "<Enter>", lambda event: self.config(cursor="bottom_side"))
                self.tag_bind(f"{widget_id}:resize_h", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}:resize_h", "<Double-Button-1>", lambda event: self.widget_resize_height(widget_id, 0))

            # width & height resizer rectangle
            if bool(style.widget_width_resizer) and bool(style.widget_height_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_wh_color, tags=[f"{widget_id}:resize_wh", f"{widget_id}:resize_wh_w"]
                )
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_wh_color, tags=[f"{widget_id}:resize_wh", f"{widget_id}:resize_wh_h"]
                )
                self.tag_bind(f"{widget_id}:resize_wh", "<Enter>", lambda event: self.config(cursor="bottom_right_corner"))
                self.tag_bind(f"{widget_id}:resize_wh", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}:resize_wh", "<Double-Button-1>", lambda event: self.widget_resize(widget_id, 0, 0))

        self.widget_reset(widget_id)


    def widget_reset(self, widget_id:str) -> None:
        """
        Resize, reposition a widget on canvas

        Args:
        widget_id (str): Widget id that will reset

        Returns:
        int: The product of a and b.
        """
        self.update()
        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id)
        self.widget_resizer_set(widget_id)
        self.update()

        resizerwh_box = self.bbox(f"{widget_id}:resize_wh")
        canvasx = resizerwh_box[2]
        canvasy = resizerwh_box[3]
        self.widget_resize_width(widget_id, 0, canvasx)
        self.widget_resize_height(widget_id, 0, canvasy)

        plugin_container = plugincontainer.get(widget_id)
        for plugin_object in plugin_container.plugins_get().values():
            plugin_object.datalabels_box_set()
            plugin_object.connect()


    # set position and size of widget name
    def widget_name_set(self, widget_id):
        move_box = self.bbox(f"{widget_id}:move")
        self.coords(f"{widget_id}:name", move_box[2] + style.widget_padding, move_box[1])


    # set position and size of plugin container
    def widget_plugin_container_set(self, widget_id):
        move_box = self.bbox(f"{widget_id}:move")
        self.coords(f"{widget_id}:plugincontainer", move_box[0], move_box[3] + style.widget_padding)


    # set position and size of background
    def widget_background_set(self, widget_id, move=False, right_side=None, bottom_side=None):
        move_box = self.bbox(f"{widget_id}:move")
        background_box = self.bbox(f"{widget_id}:background")

        outline = 1
        if self.itemcget(f"{widget_id}:background", "outline") == "":
            outline = 0

        background_box_width = background_box[2] - background_box[0] - outline * 2
        background_box_height = background_box[3] - background_box[1] - outline * 2

        if not bool(move):
            plugin_container_box = self.bbox(f"{widget_id}:plugincontainer")

            if not right_side is None:
                background_box_width = right_side - background_box[0]

            if not bottom_side is None:
                background_box_height = bottom_side - background_box[1]

            if background_box_width < style.widget_width_min:
                background_box_width = style.widget_width_min

            if background_box_height < style.widget_height_min:
                background_box_height = style.widget_height_min
            if background_box_height < plugin_container_box[3] - move_box[1] - outline * 2 + style.widget_padding * 2:
                background_box_height = plugin_container_box[3] - move_box[1] - outline * 2 + style.widget_padding * 2

        self.coords(
                f"{widget_id}:background",
                move_box[0] - style.widget_padding, move_box[1] - style.widget_padding,
                move_box[0] - style.widget_padding + background_box_width, move_box[1] - style.widget_padding + background_box_height,
            )

        return background_box_width, background_box_height


    def widget_resizer_set(self, widget_id):
        if style.widget_resizer_width > 0:
            if bool(style.widget_width_resizer) or bool(style.widget_height_resizer):
                background_box = self.bbox(f"{widget_id}:background")

                outline = 1
                if self.itemcget(f"{widget_id}:background", "outline") == "":
                    outline = 0

            # width resizer line
            if bool(style.widget_width_resizer):
                self.itemconfigure(f"{widget_id}:resize_w", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}:resize_w",
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[1] + outline,
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3]
                    )

            # height resizer line
            if bool(style.widget_height_resizer):
                self.itemconfigure(f"{widget_id}:resize_h", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}:resize_h",
                        background_box[0] + outline, background_box[3] + int(style.widget_resizer_width / 2),
                        background_box[2] + style.widget_resizer_width, background_box[3] + int(style.widget_resizer_width / 2)
                    )

            # width & height resizer rectangle
            if bool(style.widget_width_resizer) and bool(style.widget_height_resizer):
                self.itemconfigure(f"{widget_id}:resize_wh", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}:resize_wh_w",
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3] - style.widget_resizer_width * style.widget_resizer_wh_width_multiplier,
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3]
                    )
                self.coords(
                        f"{widget_id}:resize_wh_h",
                        background_box[2] - style.widget_resizer_width * style.widget_resizer_wh_width_multiplier, background_box[3] + int(style.widget_resizer_width / 2),
                        background_box[2] + style.widget_resizer_width, background_box[3] + int(style.widget_resizer_width / 2)
                    )


    def dnd_start(self, move):
        self.bind('<Motion>', self.dnd_motion)
        self.bind('<ButtonRelease-1>', self.dnd_stop)
        self.addtag_withtag('selected', tk.CURRENT)


    def dnd_motion(self, event):
        tags = self.gettags('selected')
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


    def dnd_stop(self, event):
        self.dtag('selected')    # removes the 'selected' tag
        self.unbind('<Motion>')


    def widget_resize(self, widget_id, x, y):
        self.widget_resize_width(widget_id, x)
        self.widget_resize_height(widget_id, y)


    def widget_resize_width(self, widget_id, x = None, canvasx = None):
        canvas_x = None

        if not x is None:
            if x > self.winfo_width():
                self.xview_scroll(1, 'units')
            if x < 1:
                self.xview_scroll(-1, 'units')
            canvas_x = self.canvasx(x)

        if not canvasx is None:
            canvas_x = canvasx

        if not canvas_x is None:
            bg_w, _ = self.widget_background_set(widget_id, right_side=canvas_x)

            self.itemconfigure(f"{widget_id}:plugincontainer", width=bg_w - style.widget_padding * 2)

            self.widget_resizer_set(widget_id)

            self.update()

            plugin_container = plugincontainer.get(widget_id)
            for plugin_object in plugin_container.plugins_get().values():
                plugin_object.datalabels_box_set()
                plugin_object.connect()


    def widget_reset_width(self, widget_id):
        self.itemconfigure(f"{widget_id}:plugincontainer", width=style.widget_width_min - style.widget_padding * 2)
        self.update()
        self.widget_background_set()
        self.widget_resizer_set()


    def widget_resize_height(self, widget_id, y = None, canvasy = None):
        canvas_y = None

        if not y is None:
            if y > self.winfo_height():
                self.yview_scroll(1, 'units')
            if y < 1:
                self.yview_scroll(-1, 'units')
            canvas_y = self.canvasy(y)

        if not canvasy is None:
            canvas_y = canvasy

        if not canvas_y is None:
            self.widget_background_set(widget_id, bottom_side=canvas_y)
            self.widget_resizer_set(widget_id)

            self.update()


    def widget_move(self, widget_id, x, y):
        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)
        if x > self.winfo_width():
            self.xview_scroll(1, 'units')
        if x < 1:
            self.xview_scroll(-1, 'units')
        if y > self.winfo_height():
            self.yview_scroll(1, 'units')
        if y < 1:
            self.yview_scroll(-1, 'units')

        if canvas_x < style.widget_padding:
            canvas_x = style.widget_padding
        if canvas_y < style.widget_padding:
            canvas_y = style.widget_padding

        self.coords(f"{widget_id}:move", canvas_x, canvas_y)

        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id, move=True)
        self.widget_resizer_set(widget_id)

        plugin_container = plugincontainer.get(widget_id)
        for plugin_object in plugin_container.plugins_get().values():
            plugin_object.datalabels_box_set()
            plugin_object.connect()
