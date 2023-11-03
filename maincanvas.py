import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import plugincontroller
import pluginframe
import pluginbase
import style



class Maincanvas(tk.Canvas):
    def __init__(self, mainwindow, **kwargs):
        super().__init__(mainwindow.frm_main, **kwargs)
        self.__image_move = ImageTk.PhotoImage(style.image_move_16)
        self.__image_settings = ImageTk.PhotoImage(style.image_setting_16)

        self.__plugin_container = {}    # contains all plugin
        self.__plugin_counter = 0
        self.__pluginframe_container = {}
        self.__pluginframe_counter = 0
        self.__mainwindow = mainwindow

        self.__last_datalabel_object = None

        self.bind('<Button-1>', self.__dnd_start_widget)


    ##
    # Plugin functions
    ##

    def plugin_add(self, plugin_name):
        '''
        Add new plugin to canvas
        '''
        widget_ids = self.cursor_widget_ids_get()

        if not bool(widget_ids):
            self.__plugin_create(plugin_name)
        elif len(widget_ids) == 1:
            self.__plugin_insert(plugin_name, widget_ids[0])
        else:
            print("too many widget are overlapped:", widget_ids)


    def __plugin_create(self, plugin_name: str):
        '''
        Add new plugin to new widget
        '''
        display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()
        pluginframe_object = self.widget_create(canvas_x, canvas_y)
        widget_id = pluginframe_object.id_get()

        plugin_id = f"{plugin_name}.{self.__plugin_counter_get()}"
        plugin_object = plugincontroller.new_object(plugin_name, plugin_id, pluginframe_object, self)
        self.__plugin_container.update({plugin_id: plugin_object})
        pluginframe_object.pluginview_insert(plugin_id, plugin_object.view_get())

        self.widget_reset(widget_id)


    def __plugin_insert(self, plugin_name: str, widget_id):
        '''
        Insert new plugin to existing widget
        '''
        pluginframe_object = self.pluginframe_get(widget_id)

        plugin_id = f"{plugin_name}.{self.__plugin_counter_get()}"
        plugin_object = plugincontroller.new_object(plugin_name, plugin_id, pluginframe_object, self)
        self.__plugin_container.update({plugin_id: plugin_object})
        pluginframe_object.pluginview_insert(plugin_id, plugin_object.view_get())

        self.widget_reset(widget_id)


    def plugin_move(self, plugin_id, pluginframe_id_target=None, plugin_id_target=None):
        '''
        Move existing plugin
        '''
        pluginframe_object = None

        plugin_object = self.plugin_get(plugin_id)
        pluginframe_object_old = plugin_object.pluginframe_get()

        if bool(pluginframe_id_target):
            # Move plugint to other existing widget
            pluginframe_object = self.pluginframe_get(pluginframe_id_target)
        else:
            if pluginframe_object_old.pluginview_count_get() > 1:
                # Move plugin to new widget
                display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()
                pluginframe_object = self.widget_create(canvas_x, canvas_y)
            else:
                # Plugin is alone so it stays in the original widget
                pluginframe_object = pluginframe_object_old
        widget_id = pluginframe_object.id_get()

        if not widget_id == pluginframe_object_old.id_get():
            # Plugin moves to other (new or existing) widget
            pluginframe_object_old.pluginview_remove(plugin_id)

            if pluginframe_object_old.pluginview_count_get() < 1:
                # Delete old widget if empty
                self.widget_delete(pluginframe_object_old.id_get())

            plugin_object.content_set(pluginframe_object)

            pluginframe_object.pluginview_insert(plugin_id, plugin_object.view_get())

        if not plugin_id == plugin_id_target:
            # Plugin moves to other position inside the widget
            if bool(plugin_id_target):
                new_position = pluginframe_object.pluginview_position_get(plugin_id_target)
            else:
                new_position = plugin_id_target
            pluginframe_object.pluginview_position_change(plugin_id, new_position)
            pluginframe_object.box_set()
            pluginframe_object.connect()

        self.widget_reset(widget_id)

        if bool(pluginframe_object_old):
            pluginframe_object_old.box_set()
            pluginframe_object_old.connect()

        if bool(pluginframe_object):
            pluginframe_object.box_set()
            pluginframe_object.connect()


    def plugin_get(self, plugin_id: str=None):
        plugin_object = None

        if bool(plugin_id):
            try:
                plugin_object = self.__plugin_container[plugin_id]
            except:
                pass
        else:
            plugin_object = self.__plugin_container

        return plugin_object


    def plugin_delete(self, plugin_id):
        plugin_object = self.plugin_get(plugin_id)
        pluginframe_object = plugin_object.pluginframe_get()
        widget_id = pluginframe_object.id_get()
        # delete all reference from inputs
        for output_key in plugin_object.output_value_get().keys():
            plugin_input_ids = self.input_find(f"{plugin_id}:{output_key}")
            if bool(plugin_input_ids):
                for plugin_input_id in plugin_input_ids:
                    plugin_id_del, input_id_del = plugin_input_id.split(':')
                    plugin_object_del = self.plugin_get(plugin_id_del)
                    plugin_object_del.input_value_delete(input_id_del)
                    # delete connection output lines
                    self.disconnect(f"{plugin_id}:{output_key}", f"{plugin_id_del}:{input_id_del}")
        # delete connection input lines
        for input_key, input_value in plugin_object.input_value_get().items():
            if bool(input_value):
                self.disconnect(input_value, f"{plugin_id}:{input_key}")
        # delete pluginview from pluginframe
        pluginframe_object.pluginview_remove(plugin_id)
        if pluginframe_object.pluginview_count_get() < 1:
            # Delete widget if empty
            self.widget_delete(widget_id)
        else:
            pluginframe_object.box_set()
            pluginframe_object.connect()
        # delete plugin
        del plugin_object
        self.__plugin_container.pop(plugin_id)


    def plugin_input_value_set(self, plugin_id, input_id, value):
        plugin_object = self.plugin_get(plugin_id)
        plugin_object.input_value_set(input_id, value)


    def plugin_input_value_get(self, plugin_id, input_id):
        plugin_object = self.plugin_get(plugin_id)
        ret = plugin_object.input_value_get(input_id)
        return ret


    def __plugin_counter_get(self) -> int:
        ret = self.__plugin_counter
        self.__plugin_counter += 1
        return ret

    ##
    # Pluginframe functions
    ##

    def pluginframe_add(self) -> str | pluginframe.Pluginframe:
        pluginframe_id = f"widget.{self.__pluginframe_counter_get()}"

        pluginframe_object = pluginframe.Pluginframe(self, pluginframe_id)
        self.__pluginframe_container.update({pluginframe_id: pluginframe_object})

        return pluginframe_object


    def pluginframe_get(self, pluginframe_id: str=None):
        pluginframe_object = None

        if bool(pluginframe_id):
            try:
                pluginframe_object = self.__pluginframe_container[pluginframe_id]
            except:
                pass
        else:
            pluginframe_object = self.__pluginframe_container

        return pluginframe_object


    def __pluginframe_counter_get(self) -> int:
        ret = self.__pluginframe_counter
        self.__pluginframe_counter += 1
        return ret


    ##
    # Widget functions
    ##

    def widget_create(self, x=0, y=0):
        if x < style.widget_padding:
            x = style.widget_padding
        if y < style.widget_padding:
            y = style.widget_padding

        pluginframe_object = self.pluginframe_add()
        widget_id = pluginframe_object.id_get()

        # mover
        self.create_image(x, y, image=self.__image_move, anchor="nw", tags=[f"{widget_id}*move"])
        self.tag_bind(f"{widget_id}*move", "<Enter>", lambda event: self.config(cursor="hand1"))
        self.tag_bind(f"{widget_id}*move", "<Leave>", lambda event: self.config(cursor=""))

        # name
        self.create_text(0, 0, text=widget_id, anchor="nw", tags=[f"{widget_id}*name"])

        # settings button
        self.create_image(x, y, image=self.__image_settings, anchor="nw", tags=[f"{widget_id}*settings"])
        self.tag_bind(f"{widget_id}*settings", "<Button-1>", lambda event: pluginframe_object.setting_mode_toggle())

        # plugin container add
        ww = style.widget_resizer_width
        if not bool(style.widget_width_resizer):
            ww = 0
        self.create_window(
                0, 0,
                window=pluginframe_object,
                anchor="nw",
                width=style.widget_width_min - style.widget_padding * 2 - ww,
                tags=f"{widget_id}*pluginframe"
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

        return pluginframe_object


    def widget_reset(self, widget_id:str) -> None:
        """
        Resize, reposition a widget on canvas

        Args:
        widget_id (str): Widget id that will reset
        """
        self.update()
        self.widget_name_set(widget_id)
        self.widget_pluginframe_set(widget_id)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_resizer_set(widget_id)
        self.widget_settings_button_set(widget_id)
        self.update()

        pluginframe_object = self.pluginframe_get(widget_id)
        pluginframe_object.box_set()
        # for plugin_object in pluginframe_object.pluginview_get().values():
        #     plugin_object.connect()


    def widget_delete(self, widget_id:str):
        pluginframe_object = self.pluginframe_get(widget_id)

        if pluginframe_object.pluginview_count_get() < 1:
            pluginframe_object.destroy()
            del pluginframe_object
            self.__pluginframe_container.pop(widget_id)
            self.delete(f"{widget_id}*move")
            self.delete(f"{widget_id}*name")
            self.delete(f"{widget_id}*settings")
            self.delete(f"{widget_id}*pluginframe")
            self.delete(f"{widget_id}*background")
            self.delete(f"{widget_id}*resize_w")
            self.delete(f"{widget_id}*resize_h")
            self.delete(f"{widget_id}*resize_wh")
        else:
            print(f"{widget_id} deletion disabled, there are some plugin in pluginframe")


    def widget_name_set(self, widget_id):
        '''
        set position and size of widget name
        '''
        move_box = self.bbox(f"{widget_id}*move")
        self.coords(f"{widget_id}*name", move_box[2] + style.widget_padding, move_box[1])


    def widget_pluginframe_set(self, widget_id):
        '''
        set position and size of plugin container
        '''
        move_box = self.bbox(f"{widget_id}*move")
        self.coords(f"{widget_id}*pluginframe", move_box[0], move_box[3] + style.widget_padding)


    def widget_background_set(self, widget_id, keep_height=False):
        '''
        set position and size of background
        '''
        move_box = self.bbox(f"{widget_id}*move")
        plugin_container_box = self.bbox(f"{widget_id}*pluginframe")
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

        # TEST
        # background_box = self.bbox(f"{widget_id}*background")
        # self.itemconfigure(f"{widget_id}*name", text=f"({background_box[0]}, {background_box[1]}) ({background_box[2]}, {background_box[3]})")
        # TEST END


    def widget_settings_button_set(self, widget_id):
        '''
        set position and size of settings button
        '''
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


    def __dnd_start_widget(self, move):
        self.bind('<Motion>', self.__dnd_motion_widget)
        self.bind('<ButtonRelease-1>', self.__dnd_stop_widget)
        self.addtag_withtag('selected', tk.CURRENT)


    def __dnd_motion_widget(self, event):
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


    def __dnd_stop_widget(self, event):
        self.dtag('selected')    # removes the 'selected' tag
        self.unbind('<Motion>')
        self.__mainwindow.statusbar_set()


    def widget_resize(self, widget_id, x, y):
        self.widget_resize_width(widget_id, x)
        self.widget_resize_height(widget_id, y)


    def widget_resize_width(self, widget_id, x):
        if x > self.winfo_width():
            self.xview_scroll(1, 'units')
        if x < 1:
            self.xview_scroll(-1, 'units')

        canvas_x = self.canvasx(x)
        pluginframe_box = self.bbox(f"{widget_id}*pluginframe")
        pluginframe_width = canvas_x - pluginframe_box[0] - style.widget_padding * 2

        ww = style.widget_resizer_width
        if not bool(style.widget_width_resizer):
            ww = 0
        if pluginframe_width < style.widget_width_min - style.widget_padding * 2 - ww:
            pluginframe_width = style.widget_width_min - style.widget_padding * 2 - ww

        self.itemconfigure(f"{widget_id}*pluginframe", width=pluginframe_width)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_resizer_set(widget_id)
        self.widget_settings_button_set(widget_id)
        self.update()

        pluginframe_object = self.pluginframe_get(widget_id)
        pluginframe_object.box_set()
        for plugin_object in pluginframe_object.pluginview_get().values():
            plugin_object.connect()


    def widget_resize_height(self, widget_id, y):
        if y > self.winfo_height():
            self.yview_scroll(1, 'units')
        if y < 1:
            self.yview_scroll(-1, 'units')

        canvas_y = self.canvasy(y)
        pluginframe_box = self.bbox(f"{widget_id}*pluginframe")

        pluginframe_height = canvas_y - pluginframe_box[1] - style.widget_padding * 2

        wh = style.widget_resizer_width
        if not bool(style.widget_height_resizer):
            wh = 0
        # a pluginframe nem lehet olyan kicsi, hogy a widget a minimum méret alá csökkenjen
        if pluginframe_height < style.widget_height_min - style.widget_padding * 2 - wh:
            pluginframe_height = style.widget_height_min - style.widget_padding * 2 - wh
        # a pluginframe nem lehet a saját tényleges méreténél kisebb
        if pluginframe_height < pluginframe_box[3] - pluginframe_box[1]:
            pluginframe_height = pluginframe_box[3] - pluginframe_box[1]

        pluginframe_object = self.pluginframe_get(widget_id)
        pluginframe_object.configure(height=pluginframe_height)
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

        x0, y0, x1, y1 = self.bbox(f"{widget_id}*background")
        items = self.find_overlapping(
                canvas_x - style.widget_padding - style.widget_resizer_width,
                canvas_y - style.widget_padding - style.widget_resizer_width,
                canvas_x + x1 - x0 - style.widget_padding,
                canvas_y + y1 - y0 - style.widget_padding
            )
        for item in items:
            w_id, w_item_type = self.gettags(item)[0].split('*')
            if not w_id == widget_id and w_item_type == "background":
                return

        self.coords(f"{widget_id}*move", canvas_x, canvas_y)

        self.widget_name_set(widget_id)
        self.widget_pluginframe_set(widget_id)
        self.widget_background_set(widget_id, keep_height=True)
        self.widget_settings_button_set(widget_id)
        self.widget_resizer_set(widget_id)

        pluginframe_object = self.pluginframe_get(widget_id)
        pluginframe_object.box_set()
        pluginframe_object.connect()


    ##
    # Connection line functions
    ##

    def connect(self, start_id, end_id):
        start_plugin_id, output_id = start_id.split(':')
        start_plugin_object = self.plugin_get(start_plugin_id)
        output_object = start_plugin_object.output_object_get(output_id)
        start_box = output_object.box_get()
        start_x = start_box[2]
        start_y = start_box[1] + ((start_box[3] - start_box[1]) / 2)

        end_plugin_id, input_id = end_id.split(':')
        end_plugin_object = self.plugin_get(end_plugin_id)
        input_object = end_plugin_object.input_object_get(input_id)
        end_box = input_object.box_get()
        end_x = end_box[0]
        end_y = end_box[1] + ((end_box[3] - end_box[1]) / 2)

        line_id = f"{start_id}-{end_id}*connect_line"

        self.connect_line_create(start_x, start_y, end_x, end_y, line_id)


    def disconnect(self, start_id, end_id):
        line_id = f"{start_id}-{end_id}*connect_line"
        self.connect_line_delete(line_id)


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
                    smooth=True, tags=tag, arrow="last", arrowshape=(16, 20, 5)
                )


    def connect_line_delete(self, tag):
        try:
            plugin_id, input_id = tag.split('*')[0].split(':')
            self.plugin_get(plugin_id).input_value_set(input_id, None)
        except:
            pass
        self.delete(tag)


    ##
    # Cursor, pointer dependent functions

    def cursor_widget_ids_get(self):
        '''
        Return widget ids under the cursor in canvas region
        '''
        ret = None

        _, _, canvas_x, canvas_y = self.cursor_position_get()

        try:
            widgets = self.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)
            widget_ids = set()
            for id in widgets:
                tags = self.gettags(id)
                if len(tags) > 0:
                    widget_id, widget_type = tags[0].split('*')
                    if widget_type == "background":
                        widget_ids.add(widget_id)
            if len(widget_ids) > 0:
                ret = list(widget_ids)
        except Exception as ex:
            print(ex)

        return ret


    def cursor_plugin_ids_get(self):
        '''
        Return plugin ids under the cursor in canvas region
        '''
        ret = None
        pluginframe_ids = self.cursor_widget_ids_get()

        if bool(pluginframe_ids):
            _, _, canvas_x, canvas_y = self.cursor_position_get()
            plugin_ids = []
            for pluginframe_id in pluginframe_ids:
                for plugin_id, pluginview_object in self.pluginframe_get(pluginframe_id).pluginview_get().items():
                    pluginview_object.box_set()
                    x1, y1, x2, y2 = pluginview_object.box_get()
                    if canvas_y >= y1 and canvas_y <= y2:
                        plugin_ids.append(plugin_id)
            if len(plugin_ids) > 0:
                ret = plugin_ids

        return ret


    def cursor_inputlabel_find(self):
        '''
        Find InputLabel under cursor
        '''
        ret = None
        input_objects = []

        display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()

        if self.is_cursor_in_canvas():
            widgets = self.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1) # widgets under cursor position

            if len(widgets) > 0:
                widget_tags = []
                for widget_id in widgets:
                    tags = self.gettags(widget_id)
                    for tag in tags:
                        widget_unpack = tag.split('*')
                        if len(widget_unpack) > 1:
                            if widget_unpack[1] == "pluginframe":
                                widget_tags.append(tag)

                widget_tags = list(set(widget_tags))

                if len(widget_tags) > 0:
                    for widget_tag in widget_tags:
                        target_widget_tag = widget_tag.split('*')[0]
                        pluginframe = self.pluginframe_get(target_widget_tag)
                        for pluginview_object in pluginframe.pluginview_get().values():
                            for input_object in pluginview_object.input_object_get().values():
                                input_box = input_object.box_get()
                                if canvas_x >= input_box[0] and canvas_x <= input_box[2] and canvas_y >= input_box[1] and canvas_y <= input_box[3]:
                                    input_objects.append(input_object)
                                    break

        if bool(input_objects):
            ret = input_objects

        return ret


    def cursor_outputlabel_find(self):
        '''
        Find OutputLabel under cursor
        '''
        ret = None
        output_objects = []

        display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()

        if self.is_cursor_in_canvas():
            widgets = self.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1) # widgets under cursor position

            if len(widgets) > 0:
                widget_tags = []
                for widget_id in widgets:
                    tags = self.gettags(widget_id)
                    for tag in tags:
                        widget_unpack = tag.split('*')
                        if len(widget_unpack) > 1:
                            if widget_unpack[1] == "pluginframe":
                                widget_tags.append(tag)

                widget_tags = list(set(widget_tags))

                if len(widget_tags) > 0:
                    for widget_tag in widget_tags:
                        target_widget_tag = widget_tag.split('*')[0]
                        pluginframe = self.pluginframe_get(target_widget_tag)
                        for pluginview_object in pluginframe.pluginview_get().values():
                            for output_object in pluginview_object.output_object_get().values():
                                output_box = output_object.box_get()
                                if canvas_x >= output_box[0] and canvas_x <= output_box[2] and canvas_y >= output_box[1] and canvas_y <= output_box[3]:
                                    output_objects.append(output_object)
                                    break

        if bool(output_objects):
            ret = output_objects

        return ret


    def cursor_position_get(self):
        '''
        Return cursor position in display and canvas
        '''
        display_x = self.winfo_pointerx() - self.winfo_rootx()
        display_y = self.winfo_pointery() - self.winfo_rooty()
        canvas_x = self.canvasx(display_x)
        canvas_y = self.canvasy(display_y)

        return (display_x, display_y, canvas_x, canvas_y)


    def is_cursor_in_canvas(self):
        '''
        Is pointer in canvas region
        '''
        display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()
        can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, self.cget("scrollregion").split()))
        if canvas_x > 0 and canvas_y > 0 and canvas_x < can_main_width - style.widget_padding * 2 and canvas_y < can_main_height - style.widget_padding * 2:
            if display_x > self.winfo_x() and display_y > self.winfo_y() and display_x < (self.winfo_x() + self.winfo_width()) and display_y < (self.winfo_y() + self.winfo_height()):
                return True
            else:
                return False
        else:
            return False


    ##
    # Other functions
    ##

    def dnd_motion_datalabel(self, event, output_id=None, input_id=None, line_tag="drawing"):
        if not bool(output_id) and not bool(input_id):
            return

        if bool(output_id) and bool(input_id):
            return

        if bool(self.__last_datalabel_object):
            # pointer leaves datalabel
            self.__last_datalabel_object.leave()
            self.__last_datalabel_object = None

        display_x, display_y, canvas_x, canvas_y = self.cursor_position_get()
        start_x = None
        start_y = None
        end_x = None
        end_y = None

        if bool(output_id):
            '''
            Ha az output_id van megadva, akkor húz egy vonalat az outputlabel-től a pointerig
            '''
            output_plugin_id, output_output_id = output_id.split(':')
            outputlabel_object = self.plugin_get(output_plugin_id).output_object_get(output_output_id)

            # draw line between outputlabel and pointer
            start_box = outputlabel_object.box_get()
            start_x = start_box[2]
            start_y = start_box[1] + ((start_box[3] - start_box[1]) / 2)

            end_x = canvas_x
            end_y = canvas_y

            datalabel_objects = self.cursor_inputlabel_find()

        if bool(input_id):
            '''
            Ha az input_id van megadva, akkor húz egy vonalat a pointertől az inputlabel-ig
            '''
            start_x = canvas_x
            start_y = canvas_y

            input_plugin_id, input_input_id = input_id.split(':')
            inputlabel_object = self.plugin_get(input_plugin_id).input_object_get(input_input_id)

            # draw line between pointer and inputlabel
            end_box = inputlabel_object.box_get()
            end_x = end_box[0]
            end_y = end_box[1] + ((end_box[3] - end_box[1]) / 2)

            datalabel_objects = self.cursor_outputlabel_find()

        self.connect_line_create(start_x, start_y, end_x, end_y, line_tag)

        if bool(datalabel_objects):
            # pointer enters datalabel object
            datalabel_object = datalabel_objects[0]
            datalabel_object.enter()
            self.__last_datalabel_object = datalabel_object


    def dnd_stop_datalabel(self, event, output_id=None, input_id=None, line_tag="drawing"):
        if not bool(output_id) and not bool(input_id):
            return

        if bool(output_id) and bool(input_id):
            return

        if bool(self.__last_datalabel_object):
            self.__last_datalabel_object = None

        self.connect_line_delete(line_tag)

        if bool(output_id):
            '''
            Ha az output_id van megadva, akkor húz egy vonalat az outputlabel-től a pointer alatt levő inputlabel-ig
            Itt az outputlabel-től kezdtük a vonal húzását
            '''
            output_plugin_id, output_output_id = output_id.split(':')
            outputlabel_object = self.plugin_get(output_plugin_id).output_object_get(output_output_id)

            input_objects = self.cursor_inputlabel_find()    # find inputlabel under cursor position
            if bool(input_objects):
                input_object = input_objects[0]
                new_value = f"{outputlabel_object.plugin_id_get()}:{outputlabel_object.id_get()}"               # new value of the input object
                old_value = self.plugin_input_value_get(input_object.plugin_id_get(), input_object.id_get())    # get old value of found inputlabel

                if not old_value == new_value:  # if value modified
                    if bool(old_value):             # if found inputlabel is not empty
                        self.disconnect(old_value, f"{input_object.plugin_id_get()}:{input_object.id_get()}")       # delete old line
                    self.plugin_input_value_set(input_object.plugin_id_get(), input_object.id_get(), new_value) # insert new value
                    self.connect(output_id, f"{input_object.plugin_id_get()}:{input_object.id_get()}")          # create new line

        if bool(input_id):
            '''
            Ha az input_id van megadva, akkor húz egy vonalat a pointer alatt levő outputlabel-től az inputlabel-ig
            Itt az inputlabel-től kezdtük a vonal húzását
            '''
            input_plugin_id, input_input_id = input_id.split(':')

            output_objects = self.cursor_outputlabel_find()    # find outputlabel under cursor position
            if bool(output_objects):
                output_object = output_objects[0]
                new_value = f"{output_object.plugin_id_get()}:{output_object.id_get()}"
                self.plugin_input_value_set(input_plugin_id, input_input_id, new_value) # insert new value, create new line
                self.connect(new_value, input_id)


    def input_find(self, value):
        '''
        Find inputs thet contain value
        '''
        ret = None
        input_ids = []

        for plugin_object in self.plugin_get().values():
            for input_id, input_value in plugin_object.input_value_get().items():
                if input_value == value:
                    input_ids.append(f"{plugin_object.id_get()}:{input_id}")

        if bool(input_ids):
            ret = input_ids

        return ret


    def run(self):
        for plugin_object in self.plugin_get().values():
            plugin_object.run()
