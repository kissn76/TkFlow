import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from PIL import Image, ImageTk
from datalabel import InputLabel, OutputLabel
import style



__container = {}
__counter = 0


def get(plugin_id):
    object = None
    try:
        object = __container[plugin_id]
    except:
        pass
    return object


def get_all():
    return __container


def get_all_as_dict():
    ret = {}
    for obj in __container.values():
        ret.update(obj.to_dict())

    return ret


def add(plugin_id, object):
    __container.update({plugin_id: object})


def counter_get():
    global __counter
    ret = __counter
    __counter += 1
    return ret



class PluginBase(ttk.Frame):
    def __init__(self, master, plugin_name, plugin_container_id, name=None, parents=[], **kwargs):
        super().__init__(master, **kwargs)
        self.parents = parents
        self.name = name
        self.id = f"{plugin_name}.{counter_get()}"
        self.plugin_container_id = plugin_container_id

        self.__input_container = {}
        self.__output_container = {}

        self.__input_row_counter = 0
        self.__output_row_counter = 0
        self.__content_row_counter = 0

        self.__gridcoulmn_input = 0
        self.__gridcolumn_setting = 1
        self.__gridcolumn_content = 2
        self.__gridcolumn_output = 3

        self.__image_setting = ImageTk.PhotoImage(style.image_setting)

        self.columnconfigure(self.__gridcolumn_content, weight=1)


    def to_dict(self):
        inputs = {}
        for input_object in self.__input_container.values():
            inputs.update(input_object.to_dict())

        outputs = {}
        for output_object in self.__output_container.values():
            outputs.update(output_object.to_dict())

        ret = {self.id: {"inputs": inputs, "outputs": outputs}}
        return ret


    def settings(self):
        print("Settings panel start", type(self), self.id)


    def content_init(self, content_object):
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1


    def settings_init(self):
        self.btn_config = tk.Button(self, image=self.__image_setting, compound="center", width=14, height=14, command=self.settings)
        self.btn_config.grid(row=0, column=self.__gridcolumn_setting)
        # self.bind('<Button-3>', self.settings)


    def input_init(self, *args):
        for var_name in args:
            input_id = f"{self.id}:{var_name}"
            self.__input_container.update({input_id: InputLabel(self, id=input_id, plugin_container_id=self.plugin_container_id)})
            self.__input_container[input_id].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
            self.__input_row_counter += 1


    # get output value that represented by input
    def input_value_get(self, input):
        input_id = f"{self.id}:{input}"
        result = None
        output_id = self.__input_container[input_id].value_get()
        if bool(output_id):
            plugin_id = output_id.split(':')[0]
            plugin_object = get(plugin_id)
            result = plugin_object.output_value_get(output_id).value_get()
        return result


    def input_container_get(self):
        return self.__input_container


    def output_init(self, *args):
        for var_name in args:
            output_id = f"{self.id}:{var_name}"
            self.__output_container.update({output_id: OutputLabel(self, id=output_id, plugin_container_id=self.plugin_container_id)})
            self.__output_container[output_id].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
            self.__output_row_counter += 1


    def output_value_get(self, output):
        return self.__output_container[output]


    def output_value_set(self, output, value):
        output_id = f"{self.id}:{output}"
        self.__output_container[output_id].value_set(text=str(value))


    def output_container_get(self):
        return self.__output_container


    def output_object_get(self, output_id):
        return self.__output_container[output_id]


    def connect(self):
        for input_object in self.__input_container.values():
            input_object.connect()

        for output_object in self.__output_container.values():
            output_object.connect()


    def datalabels_box_set(self):
        for input_object in self.__input_container.values():
            input_object.box_set()

        for output_object in self.__output_container.values():
            output_object.box_set()
