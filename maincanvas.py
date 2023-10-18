import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import plugincontroller
import plugincontainer
import pluginbase
import style



class Maincanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.image_move = ImageTk.PhotoImage(style.image_move_16)
        self.image_settings = ImageTk.PhotoImage(style.image_setting_16)
        self.__plugin_container = {}    # contains all plugin
        self.__plugin_counter = 0
        self.__plugincontainer_container = {}
        self.__plugincontainer_counter = 0


    def plugin_add(self, plugin_name: str, plugincontainer: plugincontainer.Plugincontainer):
        plugin_id = f"{plugin_name}.{self.__plugin_counter_get()}"

        plugin_base = plugincontroller.new_object(plugin_name, plugin_id, plugincontainer.id, self, master=plugincontainer)
        plugin_object = plugin_base.view_get()
        plugin_object.pack(anchor="nw", fill=tk.BOTH)
        plugin_object.setting_mode_set(plugincontainer.setting_mode_get())

        self.__plugin_container.update({plugin_id: plugin_base})
        plugincontainer.plugin_insert(plugin_id, plugin_object)


    def plugin_get(self, plugin_id: str) -> pluginbase.Pluginbase:
        plugin_object = None
        try:
            plugin_object = self.__plugin_container[plugin_id]
        except:
            pass
        return plugin_object


    def plugin_get_all(self) -> dict:
        return self.__plugin_container


    def plugin_box_set_all(self):
        for plugin_object in self.plugin_get_all().values():
            plugin_object.box_set()


    def __plugin_counter_get(self) -> int:
        ret = self.__plugin_counter
        self.__plugin_counter += 1
        return ret


    def plugincontainer_add(self) -> str | plugincontainer.Plugincontainer:
        plugincontainer_id = f"widget.{self.__plugincontainer_counter_get()}"

        plugincontainer_object = plugincontainer.Plugincontainer(self, plugincontainer_id)
        self.__plugincontainer_container.update({plugincontainer_id: plugincontainer_object})

        return plugincontainer_id, plugincontainer_object


    def plugincontainer_get(self, plugincontainer_id: str) -> plugincontainer.Plugincontainer:
        plugincontainer_object = None
        try:
            plugincontainer_object = self.__plugincontainer_container[plugincontainer_id]
        except:
            pass
        return plugincontainer_object


    def __plugincontainer_counter_get(self) -> int:
        ret = self.__plugincontainer_counter
        self.__plugincontainer_counter += 1
        return ret


    # create new widget
    def widget_create(self, plugin_name, x=24, y=24):
        if x < style.widget_padding:
            x = style.widget_padding
        if y < style.widget_padding:
            y = style.widget_padding

        widget_id, plugincontainer = self.plugincontainer_add()

        # mover
        self.create_image(x, y, image=self.image_move, anchor="nw", tags=[f"{widget_id}*move"])
        self.tag_bind(f"{widget_id}*move", "<Enter>", lambda event: self.config(cursor="hand1"))
        self.tag_bind(f"{widget_id}*move", "<Leave>", lambda event: self.config(cursor=""))

        # name
        self.create_text(0, 0, text=widget_id, anchor="nw", tags=[f"{widget_id}*name"])

        # settings button
        self.create_image(x, y, image=self.image_settings, anchor="nw", tags=[f"{widget_id}*settings"])
        self.tag_bind(f"{widget_id}*settings", "<Button-1>", lambda event: plugincontainer.setting_mode_toggle())

        # plugin container add
        ww = style.widget_resizer_width
        if not bool(style.widget_width_resizer):
            ww = 0
        self.create_window(
                0, 0,
                window=plugincontainer,
                anchor="nw",
                width=style.widget_width_min - style.widget_padding * 2 - ww,
                tags=f"{widget_id}*plugincontainer"
            )

        # background
        self.create_rectangle(0, 0, 0, 0, fill=style.widget_background_color, outline=style.widget_background_outline_color, tags=[f"{widget_id}*background"])
        self.tag_lower(f"{widget_id}*background", f"{widget_id}*move")

        # widget resizer
        if style.widget_resizer_width > 0:
            # width resizer line
            if bool(style.widget_width_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_color, tags=[f"{widget_id}*resize_w"]
                )
                self.tag_bind(f"{widget_id}*resize_w", "<Enter>", lambda event: self.config(cursor="right_side"))
                self.tag_bind(f"{widget_id}*resize_w", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}*resize_w", "<Double-Button-1>", lambda event: self.widget_resize_width(widget_id, 0))

            # height resizer line
            if bool(style.widget_height_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_color, tags=[f"{widget_id}*resize_h"]
                )
                self.tag_bind(f"{widget_id}*resize_h", "<Enter>", lambda event: self.config(cursor="bottom_side"))
                self.tag_bind(f"{widget_id}*resize_h", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}*resize_h", "<Double-Button-1>", lambda event: self.widget_resize_height(widget_id, 0))

            # width & height resizer rectangle
            if bool(style.widget_width_resizer) and bool(style.widget_height_resizer) and bool(style.widget_width_height_resizer):
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_wh_color, tags=[f"{widget_id}*resize_wh", f"{widget_id}*resize_wh_w"]
                )
                self.create_line(
                    0, 0, 0, 0,
                    width=style.widget_resizer_width,
                    fill=style.widget_resizer_wh_color, tags=[f"{widget_id}*resize_wh", f"{widget_id}*resize_wh_h"]
                )
                self.tag_bind(f"{widget_id}*resize_wh", "<Enter>", lambda event: self.config(cursor="bottom_right_corner"))
                self.tag_bind(f"{widget_id}*resize_wh", "<Leave>", lambda event: self.config(cursor=""))
                self.tag_bind(f"{widget_id}*resize_wh", "<Double-Button-1>", lambda event: self.widget_resize(widget_id, 0, 0))

        self.plugin_add(plugin_name, plugincontainer)

        self.update()
        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id)
        self.widget_resizer_set(widget_id)
        self.widget_settings_button_set(widget_id)

        for plugin_object in plugincontainer.plugins_get().values():
            plugin_object.datalabels_box_set()


    def widget_reset(self, widget_id:str) -> None:
        """
        Resize, reposition a widget on canvas

        Args:
        widget_id (str): Widget id that will reset
        """
        self.update()
        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_resizer_set(widget_id)
        self.widget_settings_button_set(widget_id)
        self.update()

        plugin_container = plugincontainer.get(widget_id)
        for plugin_object in plugin_container.plugins_get().values():
            plugin_object.datalabels_box_set()
            plugin_object.connect()


    # set position and size of widget name
    def widget_name_set(self, widget_id):
        move_box = self.bbox(f"{widget_id}*move")
        self.coords(f"{widget_id}*name", move_box[2] + style.widget_padding, move_box[1])


    # set position and size of plugin container
    def widget_plugin_container_set(self, widget_id):
        move_box = self.bbox(f"{widget_id}*move")
        self.coords(f"{widget_id}*plugincontainer", move_box[0], move_box[3] + style.widget_padding)


    # set position and size of background
    def widget_background_set(self, widget_id, keep_height=False):
        move_box = self.bbox(f"{widget_id}*move")
        plugin_container_box = self.bbox(f"{widget_id}*plugincontainer")
        background_box = self.bbox(f"{widget_id}*background")

        outline = 1
        if self.itemcget(f"{widget_id}*background", "outline") == "":
            outline = 0

        y2 = plugin_container_box[3] + style.widget_padding

        if bool(keep_height):
            height = background_box[3] - background_box[1] - outline * 2
            y2_tmp = move_box[1] - style.widget_padding + height

            if y2_tmp > y2:
                y2 = y2_tmp

        self.coords(
                f"{widget_id}*background",
                move_box[0] - style.widget_padding, move_box[1] - style.widget_padding,
                plugin_container_box[2] + style.widget_padding, y2
            )


    # set position and size of settings button
    def widget_settings_button_set(self, widget_id):
        move_box = self.bbox(f"{widget_id}*move")
        background_box = self.bbox(f"{widget_id}*background")
        settings = self.bbox(f"{widget_id}*settings")
        width = settings[2] - settings[0]

        self.coords(
                f"{widget_id}*settings",
                background_box[2] - width - style.widget_padding, move_box[1]
            )


    def widget_resizer_set(self, widget_id):
        if style.widget_resizer_width > 0:
            if bool(style.widget_width_resizer) or bool(style.widget_height_resizer):
                background_box = self.bbox(f"{widget_id}*background")

                outline = 1
                if self.itemcget(f"{widget_id}*background", "outline") == "":
                    outline = 0

            # width resizer line
            if bool(style.widget_width_resizer):
                self.itemconfigure(f"{widget_id}*resize_w", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}*resize_w",
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[1] + outline,
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3]
                    )

            # height resizer line
            if bool(style.widget_height_resizer):
                self.itemconfigure(f"{widget_id}*resize_h", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}*resize_h",
                        background_box[0] + outline, background_box[3] + int(style.widget_resizer_width / 2),
                        background_box[2] + style.widget_resizer_width, background_box[3] + int(style.widget_resizer_width / 2)
                    )

            # width & height resizer rectangle
            if bool(style.widget_width_resizer) and bool(style.widget_height_resizer) and bool(style.widget_width_height_resizer):
                self.itemconfigure(f"{widget_id}*resize_wh", width=style.widget_resizer_width)
                self.coords(
                        f"{widget_id}*resize_wh_w",
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3] - style.widget_resizer_width * style.widget_resizer_wh_width_multiplier,
                        background_box[2] + int(style.widget_resizer_width / 2), background_box[3]
                    )
                self.coords(
                        f"{widget_id}*resize_wh_h",
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
            widget_id, widget_function = tags[0].split('*')
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


    def widget_resize_width(self, widget_id, x):
        if x > self.winfo_width():
            self.xview_scroll(1, 'units')
        if x < 1:
            self.xview_scroll(-1, 'units')

        canvas_x = self.canvasx(x)
        plugincontainer_box = self.bbox(f"{widget_id}*plugincontainer")
        plugincontainer_width = canvas_x - plugincontainer_box[0] - style.widget_padding * 2

        ww = style.widget_resizer_width
        if not bool(style.widget_width_resizer):
            ww = 0
        if plugincontainer_width < style.widget_width_min - style.widget_padding * 2 - ww:
            plugincontainer_width = style.widget_width_min - style.widget_padding * 2 - ww

        self.itemconfigure(f"{widget_id}*plugincontainer", width=plugincontainer_width)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_resizer_set(widget_id)
        self.widget_settings_button_set(widget_id)
        self.update()

        plugincontainer = self.plugincontainer_get(widget_id)
        for plugin_object in plugincontainer.plugins_get().values():
            plugin_object.datalabels_box_set()
            plugin_object.connect()


    def widget_resize_height(self, widget_id, y):
        if y > self.winfo_height():
            self.yview_scroll(1, 'units')
        if y < 1:
            self.yview_scroll(-1, 'units')

        canvas_y = self.canvasy(y)
        plugincontainer_box = self.bbox(f"{widget_id}*plugincontainer")

        plugincontainer_height = canvas_y - plugincontainer_box[1] - style.widget_padding * 2

        wh = style.widget_resizer_width
        if not bool(style.widget_height_resizer):
            wh = 0
        # a plugincontainer nem lehet olyan kicsi, hogy a widget a minimum méret alá csökkenjen
        if plugincontainer_height < style.widget_height_min - style.widget_padding * 2 - wh:
            plugincontainer_height = style.widget_height_min - style.widget_padding * 2 - wh
        # a plugincontainer nem lehet a saját tényleges méreténél kisebb
        if plugincontainer_height < plugincontainer_box[3] - plugincontainer_box[1]:
            plugincontainer_height = plugincontainer_box[3] - plugincontainer_box[1]

        plugincontainer = self.plugincontainer_get(widget_id)
        plugincontainer.configure(height=plugincontainer_height)
        self.widget_background_set(widget_id)
        self.widget_resizer_set(widget_id)


    def widget_move(self, widget_id, x, y):
        if x > self.winfo_width():
            self.xview_scroll(1, 'units')
        if x < 1:
            self.xview_scroll(-1, 'units')
        if y > self.winfo_height():
            self.yview_scroll(1, 'units')
        if y < 1:
            self.yview_scroll(-1, 'units')

        canvas_x = self.canvasx(x)
        canvas_y = self.canvasy(y)

        if canvas_x < style.widget_padding:
            canvas_x = style.widget_padding
        if canvas_y < style.widget_padding:
            canvas_y = style.widget_padding

        self.coords(f"{widget_id}*move", canvas_x, canvas_y)

        self.widget_name_set(widget_id)
        self.widget_plugin_container_set(widget_id)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_settings_button_set(widget_id)
        self.widget_resizer_set(widget_id)

        plugincontainer = self.plugincontainer_get(widget_id)
        for plugin_object in plugincontainer.plugins_get().values():
            plugin_object.datalabels_box_set()
            plugin_object.connect()


    def connect_line_create(self, start_x, start_y, end_x, end_y, tag):
        offset = (end_x - start_x) / 3
        mid_0_x = start_x + offset
        mid_0_y = start_y
        mid_1_x = end_x - offset
        mid_1_y = end_y

        if len(self.find_withtag(tag)) > 0:
            self.coords(
                    tag,
                    start_x, start_y,
                    mid_0_x, mid_0_y,
                    mid_1_x, mid_1_y,
                    end_x, end_y
                )
        else:
            self.create_line(
                    start_x, start_y,
                    mid_0_x, mid_0_y,
                    mid_1_x, mid_1_y,
                    end_x, end_y,
                    smooth=True, tags=tag
                )

            # self.tag_bind(tag, "<Button-1>", lambda event: mainwindow.can_main.itemconfigure(tag, fill="red", width=6))
            self.tag_bind(tag, "<Double-Button-1>", lambda event: self.connect_line_delete(tag))


    def connect_line_delete(self, tag):
        try:
            plugin_id, input_id = tag.split('*')[0].split(':')
            self.plugin_get(plugin_id).input_value_set(input_id, None)
        except:
            pass
        self.delete(tag)


    def run(self):
        for plugin_object in self.plugin_get_all().values():
            plugin_object.run()