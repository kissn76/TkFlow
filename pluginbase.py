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

    def input_value_set(self, input_id, value):
        self.__input_value_container[input_id] = value


    def input_value_get(self, input_id=None):
        '''
        Return:
            None  - input_id doesn't exist
            dict  - input_id is None
            value - input_id exists
        '''
        ret = None
        if input_id == None:
            ret = self.__input_value_container.copy()
        else:
            if input_id in self.__input_value_container.keys():
                ret = self.__input_value_container[input_id]

        return ret


    def input_value_delete(self, input_id=None):
        if input_id == None:
            for key in self.__input_value_container.keys():
                self.input_value_set(key, None)
        else:
            if input_id in self.__input_value_container.keys():
                self.input_value_set(input_id, None)


    def input_value_pop(self, input_id=None):
        if input_id == None:
            self.__input_value_container.clear()
        else:
            if input_id in self.__input_value_container.keys():
                self.__input_value_container.pop(input_id)

    ##
    # Output functions
    ##

    def output_value_set(self, output_id, value):
        self.__output_value_container[output_id] = value


    def output_value_get(self, output_id=None):
        ret = None
        if output_id == None:
            ret = self.__output_value_container.copy()
        else:
            if output_id in self.__output_value_container.keys():
                ret = self.__output_value_container[output_id]

        return ret


    def output_value_delete(self, output_id=None):
        if output_id == None:
            for key in self.__output_value_container.keys():
                self.output_value_set(key, None)
        else:
            if output_id in self.__output_value_container.keys():
                self.output_value_set(output_id, None)

    ##
    # Setting functions
    ##

    def setting_value_set(self, setting_id, value):
        self.__setting_value_container[setting_id] = value


    def setting_value_get(self, setting_id=None):
        ret = None
        if setting_id == None:
            ret = self.__setting_value_container.copy()
        else:
            if setting_id in self.__setting_value_container.keys():
                ret = self.__setting_value_container[setting_id]

        return ret


    def setting_value_delete(self, setting_id=None):
        if setting_id == None:
            for key in self.__setting_value_container.keys():
                self.setting_value_set(key, None)
        else:
            if setting_id in self.__setting_value_container.keys():
                self.setting_value_set(setting_id, None)



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
        self.__settings_view = PluginbaseSettingsView(self.winfo_toplevel(), model)
        self.__setting_frame = ttk.Frame(self)
        self.__setting_mode = False

        self.__floating_widget = None
        self.__plugin_label = ttk.Label(self, text=self.id_get())

        self.__contentrow_label_widget_container = {}
        self.__input_container = {}
        self.__output_container = {}
        self.__inputlist_counter = {}

        self.__output_row_counter = 1
        self.__content_row_counter = 0

        self.__gridcoulmn_input = 0
        self.__gridcolumn_content_label = 1
        self.__gridcolumn_content = 2
        self.__gridcolumn_output = 3

        self.__image_setting = ImageTk.PhotoImage(style.image_setting_12)
        self.__image_arranger = ImageTk.PhotoImage(style.image_arranger_12)
        self.__image_delete = ImageTk.PhotoImage(style.image_delete_12)
        self.__image_move = ImageTk.PhotoImage(style.image_move_12)

        self.columnconfigure(self.__gridcolumn_content, weight=1)

        self.contentrow_init(self.__plugin_label)
        self.settingvariable_init("__system_pluginlabel__", self.id_get())
        self.settingvariable_init("__system_pluginlabel_show__", True)
        self.settingrow_init("entry", "__system_pluginlabel__", "Plugin label")
        self.settingrow_init("checkbutton", "__system_pluginlabel_show__", "Plugin label show")

        self.button_arranger_init()
        self.button_settings_init()
        self.button_delete_init()

        self.settingsview_get().savebtn_configure(self.setting_save)


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


    def pluginlabel_set(self):
        if self.settingvariable_get("__system_pluginlabel_show__") == False:
            self.__plugin_label.grid_remove()
        else:
            self.__plugin_label.configure(text=self.settingvariable_get("__system_pluginlabel__"))
            self.__plugin_label.grid(row=0, column=0, columnspan=4, sticky="we")

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
        self.arranger = ttk.Frame(self.__setting_frame)
        self.btn_arranger = tk.Button(self.arranger, image=self.__image_move, compound=tk.CENTER)
        self.btn_arranger.pack()
        self.arranger.pack(side=tk.LEFT)
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
        self.config = ttk.Frame(self.__setting_frame)
        self.btn_config = tk.Button(self.config, image=self.__image_setting, compound=tk.CENTER)
        self.btn_config.pack()
        self.config.pack(side=tk.LEFT)
        self.btn_config.bind('<Button-1>', self.__frame_settings_open)


    def __frame_settings_open(self, event):
        widget_id = self.pluginframe_get().id_get()
        background_box = self.__canvas.bbox(f"{widget_id}*background")
        self.__settings_view.open(background_box[0], background_box[1])


    def button_delete_init(self):
        self.delete = ttk.Frame(self.__setting_frame)
        self.btn_delete = tk.Button(self.delete, image=self.__image_delete, compound=tk.CENTER)
        self.btn_delete.pack()
        self.delete.pack(side=tk.LEFT)
        self.btn_delete.bind('<Button-1>', lambda event: self.__canvas.plugin_delete(self.id_get()))


    def setting_mode_set(self, setting_mode):
        self.__setting_mode = setting_mode
        if not setting_mode:
            self.__setting_frame.place_forget()
        else:
            self.__setting_frame.place(x=0, y=0)
            self.__setting_frame.lift()

        for input_object in self.input_object_get().values():
            input_object.setting_mode_set(self.__setting_mode)

    ##
    # Content functions
    ##

    def contentrow_init(self, content_object, row_label=""):
        if self.__content_row_counter > 0:
            id = f"__system_content_label_{self.__content_row_counter}"
            id_show = f"__system_content_label_{self.__content_row_counter}_show"
            self.settingvariable_init(id, row_label)
            self.settingvariable_init(id_show, True)
            if row_label == "":
                row_label = f"Label {self.__content_row_counter}"
            else:
                row_label = f"Label {row_label}"
            self.settingrow_init("entry", id, row_label)
            self.settingrow_init("checkbutton", id_show, f"{row_label} show")
            contentrow_label = ttk.Label(self, text=self.settingvariable_get(id))
            contentrow_label.grid(row=self.__content_row_counter, column=self.__gridcolumn_content_label)
            self.__contentrow_label_widget_container.update({id: contentrow_label})
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1
        self.setting_save()


    def contentrow_label_widget_set(self):
        for content_label_id, content_label_object in self.__contentrow_label_widget_container.items():
            if self.settingvariable_get(f"{content_label_id}_show") == True:
                content_label_object.configure(text=self.settingvariable_get(content_label_id))
            else:
                content_label_object.configure(text="")

    ##
    # Input functions
    ##

    def inputlist_init(self, input_id_prefix, max_element=0, setting_enabled=True):
        if not input_id_prefix in self.__inputlist_counter.keys():
            self.__inputlist_counter.update({input_id_prefix: 0})

            settingvariable_id = f"__system_inputlist_max_element_{input_id_prefix}"
            if self.settingvariable_get(settingvariable_id) == None:
                self.settingvariable_init(settingvariable_id, max_element)

                if setting_enabled:
                    self.settingrow_init("entry", settingvariable_id, f"Max number of {input_id_prefix}")

                self.inputlist_max_element_set(input_id_prefix, max_element)

            self.inputlist_append(input_id_prefix)


    def inputlist_max_element_set(self, input_id_prefix, max_element=0):
        # TODO
        # Inputlabel-ek kezelése
        #   - csökkentéskor inputlabelek törlése
        #       - ha üresek
        #       - mi van ha van bennük érték?

        settingvariable_id = f"__system_inputlist_max_element_{input_id_prefix}"

        if self.settingvariable_get(settingvariable_id) == None:
            self.settingvariable_init(settingvariable_id, max_element)
            self.settingrow_init("entry", settingvariable_id, f"Max number of {input_id_prefix}")
        else:
            if max_element == 'e':
                self.inputlist_clean(input_id_prefix)
                max_element = 1
                self.settingvariable_set(settingvariable_id, int(max_element))

            if max_element == None or int(max_element) <= 0:
                max_element = 0
                self.settingvariable_set(settingvariable_id, int(max_element))

            if int(max_element) > 0 and len(self.inputlist_get(input_id_prefix)) > int(max_element): # több az inputlabel mint amennyi kéne
                max_element = len(self.inputlist_get(input_id_prefix))
                print("WARNING - too much input element exists")
            elif int(max_element) == 0 or len(self.inputlist_get(input_id_prefix)) < int(max_element): # kevesebb az inputlabel, mint amennyit szeretnénk
                # van-e üres inputlabel?
                #   igen, nem kell csinálni semmit
                #   nem, kell egyet hozzáadni
                if not len(self.inputlist_empty_get(input_id_prefix)) > 0:
                    self.inputlist_append(input_id_prefix)
            else: # pont annyi inputlabel van amennyit szeretnénk, nem kell csinálni semmit
                pass

            self.settingvariable_set(settingvariable_id, int(max_element))


    def inputlist_append(self, input_id_prefix):
        max_element_id = f"__system_inputlist_max_element_{input_id_prefix}"

        if input_id_prefix in self.__inputlist_counter.keys():
            if self.settingvariable_get(max_element_id) == None \
                    or int(self.settingvariable_get(max_element_id)) <= 0 \
                    or len(self.inputlist_get(input_id_prefix)) < int(self.settingvariable_get(max_element_id)):
                input_id = f"{input_id_prefix}.{self.__inputlist_counter[input_id_prefix]}"
                self.inputvariable_init(input_id)
                self.__inputlist_counter[input_id_prefix] += 1


    def inputlist_pop(self, input_id):
        '''
        Delete input element. Inputvariable and inputlabel, if empty, and not only empty element.
        '''
        input_id_prefix = input_id.split('.')[0]

        empty = self.inputlist_empty_get(input_id_prefix)

        if not input_id in empty.keys():
            return

        empty.pop(input_id)
        if len(empty) > 0:
            self.inputvariable_pop(input_id)


    def inputlist_get(self, input_id_prefix):
        ret = {}
        if input_id_prefix in self.__inputlist_counter.keys():
            input_elements = self.inputvariable_get()
            for input_id, input_value in input_elements.items():
                if input_id.startswith(input_id_prefix):
                    ret.update({input_id: input_value})

        return ret


    def inputlist_empty_get(self, input_id_prefix):
        ret = {}
        input_elements = self.inputlist_get(input_id_prefix)
        for input_id, input_value in input_elements.items():
            if (input_value == None or input_value == ""):
                ret.update({input_id: input_value})

        return ret


    def inputlist_clean(self, input_id_prefix, exclude=[]):
        '''
        Delete empty inputlabels from inputlist
        '''
        for input_id in self.inputlist_empty_get(input_id_prefix).keys():
            if not input_id in exclude:
                self.inputvariable_pop(input_id)


    def inputvariable_init(self, input_id, value=None):
        if not bool(self.inputvariable_get(input_id)):
            self.inputvariable_set(input_id, value)

        if not bool(self.input_object_get(input_id)):
            self.__input_container.update({input_id: InputLabel(self, id=input_id, pluginframe_object=self.__pluginframe, canvas_object=self.__canvas)})
            self.input_object_get(input_id).setting_mode_set(self.__setting_mode)

        self.inputlabels_reset()


    def inputlabels_reset(self):
        for input_id, input_object in self.__input_container.items():
            input_object.grid_forget()

        input_row_counter = 1

        for input_id, input_object in self.__input_container.items():
            input_object.grid(row=input_row_counter, column=self.__gridcoulmn_input)
            input_row_counter += 1


    def input_object_get(self, input_id=None):
        '''
        Get input view object
        '''
        ret = None

        if bool(input_id):
            if input_id in self.__input_container.keys():
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


    def inputvariable_pop(self, input_id=None):
        '''
        Delete inputvariable and inputlabel
        '''
        self.__model.input_value_pop(input_id)
        self.__input_container[input_id].grid_forget()
        self.__input_container[input_id].destroy()
        self.__input_container.pop(input_id)

        self.inputlabels_reset()


    def input_value_get(self, input_id):
        '''
        get output value that represented by input
        '''
        result = None
        input_value = self.inputvariable_get(input_id)
        if bool(input_value):
            plugin_id, output_id  = input_value.split(':')
            result = self.__canvas.plugin_get(plugin_id).outputvariable_get(output_id)
        return result

    ##
    # Output functions
    ##

    def outputvariable_init(self, output_id, value=None):
        if not bool(self.outputvariable_get(output_id)):
            self.outputvariable_set(output_id, value)

        if not bool(self.output_object_get(output_id)):
            self.__output_container.update({output_id: OutputLabel(self, id=output_id, pluginframe_object=self.__pluginframe, canvas_object=self.__canvas)})
            self.__output_container[output_id].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
            self.__output_row_counter += 1


    def output_object_get(self, output_id=None):
        ret = None

        if bool(output_id):
            if output_id in self.__output_container.keys():
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

    def settingvariable_init(self, setting_id, value=None):
        if not bool(self.settingvariable_get(setting_id)):
            self.settingvariable_set(setting_id, value)


    def settingvariable_set(self, setting_id, value):
        self.__model.setting_value_set(setting_id, value)


    def settingvariable_get(self, setting_id=None):
        return self.__model.setting_value_get(setting_id)


    def settingsview_get(self):
        return self.__settings_view


    def settingrow_init(self, row_type, variable_name, row_label_text):
        self.settingsview_get().content_init(row_type, variable_name, row_label_text)


    def setting_save(self):
        self.settingsview_get().save()
        self.pluginlabel_set()
        self.contentrow_label_widget_set()

        for input_id_prefix in self.__inputlist_counter.keys():
            value = self.settingvariable_get(f"__system_inputlist_max_element_{input_id_prefix}")
            self.inputlist_max_element_set(input_id_prefix, value)

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

        self.__gridcolumn_label = 0
        self.__gridcolumn_content = 1

        self.__content_row_counter = 0

        ttk.Label(self, text=model.id_get()).pack()
        self.__main_frame = ttk.Frame(self)
        self.__main_frame.pack()
        ttk.Button(self, text="Cancel", command=self.close).pack(side="left")
        self.save_btn = ttk.Button(self, text="Save", command=self.save)
        self.save_btn.pack(side="right")


    def savebtn_configure(self, command):
        self.save_btn.configure(command=command)


    def open(self, x=0, y=0):
        for variable_name, row_object in self.__setting_rows.items():
            if self.__setting_rows_properties[variable_name]["type"] == "entry":
                row_object.delete(0, "end")
                row_object.insert(0, self.__model.setting_value_get(variable_name))
            elif self.__setting_rows_properties[variable_name]["type"] == "checkbutton":
                self.__setting_rows_properties[variable_name]["variable"].set(self.__model.setting_value_get(variable_name))
        self.place(x=x, y=y)


    def close(self):
        self.place_forget()


    def save(self):
        for variable_name, row_object in self.__setting_rows.items():
            row_value = None
            if self.__setting_rows_properties[variable_name]["type"] == "entry":
                row_value = row_object.get()
            elif self.__setting_rows_properties[variable_name]["type"] == "checkbutton":
                row_value = self.__setting_rows_properties[variable_name]["variable"].get()

            self.__model.setting_value_set(variable_name, row_value)

        self.close()


    def content_init(self, row_type, variable_name, row_label_text):
        self.__setting_rows_properties.update({variable_name: {"type": row_type, "label": row_label_text, "variable": None}})
        label = ttk.Label(self.__main_frame, text=row_label_text)
        label.grid(row=self.__content_row_counter, column=self.__gridcolumn_label, sticky="we")

        content_object = None
        if row_type == "entry":
            content_object = ttk.Entry(self.__main_frame)
            content_object.delete(0, "end")
            content_object.insert(0, str(self.__model.setting_value_get(variable_name)))
            content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        elif row_type == "checkbutton":
            cb_value = tk.BooleanVar()
            cb_value.set(self.__model.setting_value_get(variable_name))
            self.__setting_rows_properties[variable_name]["variable"] = cb_value
            content_object = ttk.Checkbutton(self.__main_frame, onvalue=True, offvalue=False, variable=cb_value)
            content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="w")

        if bool(content_object):
            self.__setting_rows.update({variable_name: content_object})
            self.__content_row_counter += 1
