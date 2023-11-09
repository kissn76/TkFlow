import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from datalabel import InputLabel, OutputLabel
import style
import pluginframe
import maincanvas



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


    ##
    # Input functions
    ##

    def input_value_set(self, input, value):
        self.__input_value_container[input] = value


    def input_value_get(self, input=None):
        ret = None
        if bool(input) and input in self.__input_value_container.keys():
            ret = self.__input_value_container[input]
        else:
            ret = self.__input_value_container.copy()

        return ret


    def input_value_delete(self, input=None):
        if not bool(input):
            for key in self.__input_value_container.keys():
                self.input_value_set(key, None)
        else:
            if input in self.__input_value_container.keys():
                self.input_value_set(input, None)


    ##
    # Output functions
    ##

    def output_value_set(self, output, value):
        self.__output_value_container[output] = value


    def output_value_get(self, output=None):
        ret = None
        if bool(output) and output in self.__output_value_container.keys():
            ret = self.__output_value_container[output]
        else:
            ret = self.__output_value_container.copy()

        return ret


    def output_value_delete(self, output=None):
        if not bool(output):
            for key in self.__output_value_container.keys():
                self.output_value_set(key, None)
        else:
            if output in self.__output_value_container.keys():
                self.output_value_set(output, None)


    ##
    # Setting functions
    ##

    def setting_value_set(self, setting, value):
        self.__setting_value_container[setting] = value


    def setting_value_get(self, setting=None):
        ret = None
        if bool(setting) and setting in self.__setting_value_container.keys():
            ret = self.__setting_value_container[setting]
        else:
            ret = self.__setting_value_container.copy()

        return ret


    def setting_value_delete(self, setting=None):
        if not bool(setting):
            for key in self.__setting_value_container.keys():
                self.setting_value_set(key, None)
        else:
            if setting in self.__setting_value_container.keys():
                self.setting_value_set(setting, None)



class Pluginbase(ttk.Frame):
    '''
        Pluginbase view
    '''
    def __init__(self, master: pluginframe.Pluginframe, canvas_object:maincanvas.Maincanvas, model: PluginbaseModel, **kwargs):
        super().__init__(master, **kwargs)
        self.__model = model
        self.__box = ()   # box in canvas
        self.__canvas = canvas_object
        self.__pluginframe = master
        self.settings_view = PluginbaseSettingsView(self.winfo_toplevel(), model)
        self.__settings_view_opened = False

        self.__floating_widget = None
        # self.__marker_widget = ttk.Label(self, text=f"{self.__pluginframe.id_get()}-{self.id_get()}")
        self.__marker_widget = ttk.Label(self, text=self.id_get())

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

        self.contentrow_init(self.__marker_widget)
        self.button_arranger_init()
        self.button_settings_init()
        self.button_delete_init()


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


    def pluginframe_get(self):
        return self.__pluginframe


    ##
    # Position functions
    ##

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


    ##
    # Plugin manipulation buttons
    ##

    def button_arranger_init(self):
        self.arranger = ttk.Frame(self)
        self.btn_arranger = tk.Button(self.arranger, image=self.__image_move, compound=tk.CENTER)
        self.btn_arranger.grid(row=0, column=0, sticky="nswe")
        self.btn_arranger.bind('<Button-1>', self.__dnd_arrange_start)


    def __dnd_arrange_start(self, event):
        display_x, display_y, canvas_x, canvas_y = self.__canvas.cursor_position_get()

        self.__floating_widget = ttk.Label(self.winfo_toplevel(), text=self.__model.id_get())
        self.__floating_widget.place(x=display_x, y=display_y)

        self.btn_arranger.bind('<B1-Motion>', self.__dnd_arrange_motion)
        self.btn_arranger.bind('<ButtonRelease-1>', self.__dnd_arrange_stop)


    def __dnd_arrange_motion(self, event):
        if bool(self.__floating_widget):
            display_x, display_y, canvas_x, canvas_y = self.__canvas.cursor_position_get()
            self.__floating_widget.place(x=display_x, y=display_y)


    def __dnd_arrange_stop(self, event):
        self.btn_arranger.unbind('<B1-Motion>')
        self.btn_arranger.unbind('<ButtonRelease-1>')
        if bool(self.__floating_widget):
            self.__floating_widget.place_forget()
            self.__floating_widget.destroy()
            self.__floating_widget = None

        pluginframe_target_id = self.__canvas.cursor_widget_ids_get()
        plugin_target_id = self.__canvas.cursor_plugin_ids_get()

        if bool(pluginframe_target_id):
            pluginframe_target_id = pluginframe_target_id[0]

        if bool(plugin_target_id):
            plugin_target_id = plugin_target_id[0]

        self.__canvas.plugin_move(self.id_get(), pluginframe_target_id, plugin_target_id)


    def button_settings_init(self):
        self.config = ttk.Frame(self)
        self.btn_config = tk.Button(self.config, image=self.__image_setting, compound=tk.CENTER)
        self.btn_config.grid(row=0, column=0, sticky="nswe")
        self.btn_config.bind('<Button-1>', self.__frame_settings_toggle)


    def __frame_settings_toggle(self, event):
        widget_id = self.pluginframe_get().id_get()
        background_box = self.__canvas.bbox(f"{widget_id}*background")

        if self.__settings_view_opened:
            self.settings_view.close()
            self.__settings_view_opened = False
        else:
            self.settings_view.open(background_box[0], background_box[1])
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


    def button_delete_init(self):
        self.delete = ttk.Frame(self)
        self.btn_delete = tk.Button(self.delete, image=self.__image_delete, compound=tk.CENTER)
        self.btn_delete.grid(row=0, column=0, sticky="nswe")
        self.btn_delete.bind('<Button-1>', lambda event: self.__canvas.plugin_delete(self.id_get()))


    ##
    # Content functions
    ##

    def contentrow_init(self, content_object):
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1


    ##
    # Input functions
    ##

    def inputvariable_init(self, *input_id):
        for var_name in input_id:
            if not bool(self.inputvariable_get(var_name)):
                self.inputvariable_set(var_name, None)

            if not bool(self.input_object_get(var_name)):
                self.__input_container.update({var_name: InputLabel(self, id=var_name, pluginview_object=self, pluginframe_object=self.__pluginframe, canvas_object=self.__canvas)})
                self.__input_container[var_name].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
                self.__input_row_counter += 1


    def input_object_get(self, input_id=None):
        '''
        Get input view object
        '''
        ret = None

        if bool(input_id):
            ret = self.__input_container[input_id]
        else:
            ret = self.__input_container

        return ret


    def inputvariable_get(self, input_id=None):
        return self.__model.input_value_get(input_id)


    def inputvariable_set(self, input_id, value):
        self.__model.input_value_set(input_id, value)


    def inputvariable_delete(self, input_id=None):
        self.__model.input_value_delete(input_id)


    def input_value_get(self, input_id):
        '''
        get output value that represented by input
        '''
        result = None
        input_value = self.inputvariable_get(input_id)
        if bool(input_value):
            plugin_id, output_id  = input_value.split(':')
            result = self.__canvas.plugin_get(plugin_id).output_value_get(output_id)
        return result


    ##
    # Output functions
    ##

    def outputvariable_init(self, *output_id):
        for var_name in output_id:
            if not bool(self.outputvariable_get(var_name)):
                self.outputvariable_set(var_name, None)

            if not bool(self.output_object_get(var_name)):
                self.__output_container.update({var_name: OutputLabel(self, id=var_name, pluginview_object=self, pluginframe_object=self.__pluginframe, canvas_object=self.__canvas)})
                self.__output_container[var_name].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
                self.__output_row_counter += 1


    def output_object_get(self, output_id=None):
        ret = None

        if bool(output_id) and output_id in self.__output_container.keys():
            ret = self.__output_container[output_id]
        else:
            ret = self.__output_container

        return ret


    def outputvariable_get(self, output_id=None):
        return self.__model.output_value_get(output_id)


    def outputvariable_set(self, output_id, value):
        self.__model.output_value_set(output_id, value)


    def outputvariable_delete(self, output_id=None):
        self.__model.output_value_delete(output_id)


    ##
    # Setting functions
    ##

    def settingvariable_init(self, *setting_id):
        for var_name in setting_id:
            if not bool(self.settingvariable_get(var_name)):
                self.settingvariable_set(var_name, None)


    def settingrow_init(self, row_type, variable_name, row_label_text):
        self.settings_view.content_init(row_type, variable_name, row_label_text)


    def settingvariable_set(self, setting_id, value):
        self.__model.setting_value_set(setting_id, value)


    def settingvariable_get(self, setting_id=None):
        return self.__model.setting_value_get(setting_id)


    ##
    # Other functions
    ##

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

        self.__setting_rows = {}
        self.__setting_rows_properties = {}

        self.__gridcoulmn_label = 0
        self.__gridcolumn_content = 1

        self.__content_row_counter = 0

        ttk.Label(self, text=model.id_get()).pack()
        self.__main_frame = ttk.Frame(self)
        self.__main_frame.pack()
        ttk.Button(self, text="Cancel", command=self.close).pack(side="left")
        self.save_btn = ttk.Button(self, text="Save", command=self.save)
        self.save_btn.pack(side="right")


    def open(self, x=0, y=0):
        for variable_name, row_object in self.__setting_rows.items():
            if self.__setting_rows_properties[variable_name]["type"] == "entry":
                row_object.delete(0, "end")
                row_object.insert(0, self.__model.setting_value_get(variable_name))
        self.place(x=x, y=y)


    def close(self):
        self.place_forget()


    def save(self):
        for variable_name, row_object in self.__setting_rows.items():
            row_value = None
            if self.__setting_rows_properties[variable_name]["type"] == "entry":
                row_value = row_object.get()
            self.__model.setting_value_set(variable_name, row_value)

        self.close()


    def content_init(self, row_type, variable_name, row_label_text):
        self.__setting_rows_properties.update({variable_name: {"type": row_type, "label": row_label_text}})
        label = ttk.Label(self.__main_frame, text=row_label_text)
        label.grid(row=self.__content_row_counter, column=self.__gridcoulmn_label, sticky="we")

        if row_type == "entry":
            content_object = ttk.Entry(self.__main_frame)
            content_object.delete(0, "end")
            content_object.insert(0, str(self.__model.setting_value_get(variable_name)))
            content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
            self.__content_row_counter += 1
            self.__setting_rows.update({variable_name: content_object})
