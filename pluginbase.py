import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from datalabel import InputLabel, OutputLabel
import style
import pluginframe
import maincanvas



class Pluginbase():
    '''
        Pluginbase controller
    '''
    def __init__(self, plugin_id, pluginframe_object: pluginframe.Pluginframe, canvas_object: maincanvas.Maincanvas, **kwargs):
        self.__view = None
        self.__model = PluginbaseModel(plugin_id)
        self.__canvas = canvas_object
        self.__pluginframe = pluginframe_object
        self.__settings_view = PluginbaseSettingsView(self.__canvas, self.__model)


    def id_get(self):
        return self.__model.id_get()


    def pluginframe_get(self):
        return self.__pluginframe


    def view_create(self, pluginframe_object: pluginframe.Pluginframe, **kwargs):
        self.__pluginframe = pluginframe_object
        self.__view = PluginbaseView(self.pluginframe_get(), self.__canvas, self.__model, self.__settings_view, **kwargs)
        self.__view.setting_mode_set(self.pluginframe_get().setting_mode_get())


    def view_init(self):
        for var_name in self.input_value_get().keys():
            self.__view.input_init(var_name)

        for var_name in self.output_value_get().keys():
            self.__view.output_init(var_name)


    def view_get(self):
        return self.__view


    def settings_view_get(self):
        return self.__settings_view


    def settings_content_init(self, label_text, content_object):
        self.__settings_view.content_init(label_text, content_object)


    def content_init(self, content_object):
        self.__view.content_init(content_object)


    def input_init(self, *args):
        for var_name in args:
            self.__model.input_value_set(var_name, None)


    def input_object_get(self, input):
        return self.__view.input_object_get(input)


    def input_value_set(self, input, value):
        self.__model.input_value_set(input, value)


    def input_value_delete(self, input):
        self.__model.input_value_set(input, None)


    def input_value_get(self, input=None):
        return self.__model.input_value_get(input)


    # get output value that represented by input
    def input_value_get_referenced(self, input):
        result = None
        input_value = self.__model.input_value_get(input)
        if bool(input_value):
            plugin_id, output_id  = input_value.split(':')
            plugin_object = self.__canvas.plugin_get(plugin_id)
            result = plugin_object.output_value_get(output_id)
        return result


    def output_init(self, *args):
        for var_name in args:
            self.__model.output_value_set(var_name, None)


    def output_object_get(self, output):
        return self.__view.output_object_get(output)


    def output_value_set(self, output, value):
        self.__model.output_value_set(output, value)


    def output_value_get(self, output=None):
        return self.__model.output_value_get(output)


    def setting_init(self, *args):
        for var_name in args:
            self.__model.setting_value_set(var_name, None)


    def setting_value_set(self, setting, value):
        self.__model.setting_value_set(setting, value)


    def setting_value_get(self, setting=None):
        return self.__model.setting_value_get(setting)



class PluginbaseModel():
    '''
        Pluginbase model
    '''
    def __init__(self, plugin_id):
        self.__id = plugin_id

        self.__input_value_container = {}
        self.__output_value_container = {}
        self.__setting_value_container = {}


    def id_get(self):
        return self.__id


    def input_value_set(self, input, value):
        self.__input_value_container[input] = value


    def input_value_get(self, input=None):
        ret = None
        if bool(input):
            ret = self.__input_value_container[input]
        else:
            ret = self.__input_value_container.copy()

        return ret


    def output_value_set(self, output, value):
        self.__output_value_container[output] = value


    def output_value_get(self, output=None):
        ret = None
        if bool(output):
            ret = self.__output_value_container[output]
        else:
            ret = self.__output_value_container.copy()

        return ret


    def setting_value_set(self, setting, value):
        self.__setting_value_container[setting] = value


    def setting_value_get(self, setting=None):
        ret = None
        if bool(setting):
            ret = self.__setting_value_container[setting]
        else:
            ret = self.__setting_value_container.copy()

        return ret



class PluginbaseView(ttk.Frame):
    '''
        Pluginbase view
    '''
    def __init__(self, master: pluginframe.Pluginframe, canvas_object:maincanvas.Maincanvas, model: PluginbaseModel, settings_view, **kwargs):
        super().__init__(master, **kwargs)
        self.__model = model
        self.__box = ()   # box in canvas
        self.__canvas = canvas_object
        self.__pluginframe = master
        self.__settings_view = settings_view
        self.__settings_view_opened = False

        self.__floating_widget = None
        self.__marker_widget = ttk.Label(self, text=f"{self.__pluginframe.id_get()}-{self.id_get()}")

        self.__input_container = {}
        self.__output_container = {}

        self.__input_row_counter = 0
        self.__output_row_counter = 0
        self.__content_row_counter = 0

        self.__gridcolumn_arranger = 0
        self.__gridcolumn_setting = 1
        self.__gridcolumn_delete = 2
        self.__gridcoulmn_input = 3
        self.__gridcolumn_content = 4
        self.__gridcolumn_output = 5

        self.__image_setting = ImageTk.PhotoImage(style.image_setting_12)
        self.__image_arranger = ImageTk.PhotoImage(style.image_arranger_12)
        self.__image_delete = ImageTk.PhotoImage(style.image_delete_12)
        self.__image_move = ImageTk.PhotoImage(style.image_move_12)

        self.columnconfigure(self.__gridcolumn_content, weight=1)

        self.content_init(self.__marker_widget)
        self.arranger_init()
        self.settings_init()
        self.delete_init()


    def to_dict(self):
        inputs = {}
        for input_object in self.__input_container.values():
            inputs.update(input_object.to_dict())

        outputs = {}
        for output_object in self.__output_container.values():
            outputs.update(output_object.to_dict())

        ret = {self.__model.id_get(): {"inputs": inputs, "outputs": outputs}}
        return ret


    def id_get(self):
        return self.__model.id_get()


    # set box in canvas
    def box_set(self, event=None):
        pluginframe_box = self.__canvas.bbox(f"{self.__pluginframe.id_get()}*pluginframe")
        plugin_geometry = self.winfo_geometry().replace('x', '+').split("+") # plugin geometry

        x1 = int(pluginframe_box[0]) + int(plugin_geometry[2])
        y1 = int(pluginframe_box[1]) + int(plugin_geometry[3])
        x2 = int(x1 + int(plugin_geometry[0]))
        y2 = int(y1 + int(plugin_geometry[1]))

        self.__box = (x1, y1, x2, y2)

        for input_object in self.input_object_get().values():
            input_object.box_set()

        for output_object in self.output_object_get().values():
            output_object.box_set()


    def box_get(self):
        return self.__box


    def arranger_init(self):
        self.arranger = ttk.Frame(self)
        self.btn_arranger = tk.Button(self.arranger, image=self.__image_move, compound=tk.CENTER)
        self.btn_arranger.grid(row=0, column=0, sticky="nswe")
        self.btn_arranger.bind('<Button-1>', lambda event: self.dnd_arrange_start(event))
        self.btn_arranger.bind('<B1-Motion>', lambda event: self.dnd_arrange_motion(event))
        self.btn_arranger.bind('<ButtonRelease-1>', lambda event: self.dnd_arrange_stop(event))


    def dnd_arrange_start(self, event):
        # self.leave()
        display_x, display_y, canvas_x, canvas_y = self.__canvas.cursor_position_get()

        self.__floating_widget = ttk.Label(self.winfo_toplevel(), text=self.__model.id_get())
        self.__floating_widget.place(x=display_x, y=display_y)


    def dnd_arrange_motion(self, event):
        if bool(self.__floating_widget):
            display_x, display_y, canvas_x, canvas_y = self.__canvas.cursor_position_get()
            self.__floating_widget.place(x=display_x, y=display_y)


    def dnd_arrange_stop(self, event):
        plugin_id = self.__model.id_get()
        if bool(self.__floating_widget):
            self.__floating_widget.place_forget()
            self.__floating_widget.destroy()
            self.__floating_widget = None

        display_x, display_y, canvas_x, canvas_y = self.__canvas.cursor_position_get()

        pluginframe_target_id = self.__canvas.cursor_widget_ids_get()
        plugin_target_id = self.__canvas.cursor_plugin_ids_get()

        if bool(pluginframe_target_id):
            pluginframe_target_id = pluginframe_target_id[0]

        if bool(plugin_target_id):
            plugin_target_id = plugin_target_id[0]

        self.__canvas.plugin_move(plugin_id, pluginframe_target_id, plugin_target_id, x=canvas_x, y=canvas_y)


    def settings_init(self):
        self.config = ttk.Frame(self)
        self.btn_config = tk.Button(self.config, image=self.__image_setting, compound=tk.CENTER)
        self.btn_config.grid(row=0, column=0, sticky="nswe")
        self.btn_config.bind('<Button-1>', lambda event: self.settings_open(event))


    def settings_open(self, event):
        widget_id = self.__pluginframe.id_get()
        background_box = self.__canvas.bbox(f"{widget_id}*background")
        if self.__settings_view_opened:
            self.__settings_view.close()
            self.__settings_view_opened = False
        else:
            self.__settings_view.open(background_box[0], background_box[1])
            self.__settings_view_opened = True


    def setting_mode_set(self, setting_mode):
        if not setting_mode:
            self.arranger.grid_remove()
            self.config.grid_remove()
            self.delete.grid_remove()
        else:
            self.arranger.grid(row=0, column=self.__gridcolumn_arranger, sticky="nswe")
            self.config.grid(row=0, column=self.__gridcolumn_setting, sticky="nswe")
            self.delete.grid(row=0, column=self.__gridcolumn_delete, sticky="nswe")


    def delete_init(self):
        self.delete = ttk.Frame(self)
        self.btn_delete = tk.Button(self.delete, image=self.__image_delete, compound=tk.CENTER)
        self.btn_delete.grid(row=0, column=0, sticky="nswe")
        self.btn_delete.bind('<Button-1>', lambda event: self.__canvas.plugin_delete(self.id_get()))


    def content_init(self, content_object):
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1


    def input_init(self, input_id):
        self.__input_container.update({input_id: InputLabel(self, id=input_id, plugin_id=self.__model.id_get(), pluginframe_id=self.__pluginframe.id_get(), canvas_object=self.__canvas)})
        self.__input_container[input_id].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
        self.__input_row_counter += 1


    def input_object_get(self, input_id=None):
        ret = None

        if bool(input_id):
            ret = self.__input_container[input_id]
        else:
            ret = self.__input_container

        return ret


    def output_init(self, output_id):
        self.__output_container.update({output_id: OutputLabel(self, id=output_id, plugin_id=self.__model.id_get(), pluginframe_id=self.__pluginframe.id_get(), canvas_object=self.__canvas)})
        self.__output_container[output_id].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
        self.__output_row_counter += 1


    def output_object_get(self, output_id=None):
        ret = None

        if bool(output_id):
            ret = self.__output_container[output_id]
        else:
            ret = self.__output_container

        return ret


    def input_container_get(self):
        return self.__input_container


    def output_container_get(self):
        return self.__output_container


    def connect(self):
        for input_id, input_value in self.__model.input_value_get().items():
            start = input_value
            end = f"{self.id_get()}:{input_id}"
            if bool(start) and bool(end):
                self.__canvas.connect(start, end)

        for output_id in self.__model.output_value_get().keys():
            start = f"{self.id_get()}:{output_id}"
            input_ids = self.__canvas.input_find(start)
            if bool(input_ids):
                for input_id in input_ids:
                    self.__canvas.connect(start, input_id)



class PluginbaseSettingsView(ttk.Frame):
    '''
        Pluginbase settings view
    '''
    def __init__(self, master, model: PluginbaseModel, **kwargs):
        super().__init__(master, **kwargs)
        self.__model = model

        self.__gridcoulmn_label = 0
        self.__gridcolumn_content = 1

        self.__content_row_counter = 0


    def open(self, x=0, y=0):
        self.place(x=x, y=y)


    def close(self):
        self.place_forget()


    def content_init(self, label_text, content_object):
        label = ttk.Label(self, text=label_text)
        label.grid(row=self.__content_row_counter, column=self.__gridcoulmn_label, sticky="we")
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1
