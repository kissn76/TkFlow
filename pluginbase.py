import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from PIL import Image, ImageTk
from datalabel import InputLabel, OutputLabel, input_add, input_get, input_get_by_plugin, output_add, output_get, output_get_by_plugin



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


def add(plugin_id, object):
    __container.update({plugin_id: object})


def counter_get():
    global __counter
    ret = __counter
    __counter += 1
    return ret



class PluginBase(ttk.Frame):
    def __init__(self, master, plugin_name, parent_id, name=None, parents=[], **kwargs):
        super().__init__(master, **kwargs)
        self.parents = parents
        self.name = name
        self.id = f"{parent_id}:{plugin_name}.{counter_get()}"

        self.__input_row_counter = 0
        self.__output_row_counter = 0
        self.__content_row_counter = 0

        self.__gridcoulmn_input = 0
        self.__gridcolumn_setting = 1
        self.__gridcolumn_content = 2
        self.__gridcolumn_output = 3

        self.__image_setting = Image.open("./resources/icon/setting.png")
        self.__image_setting.thumbnail((16, 16))
        self.__image_setting = ImageTk.PhotoImage(self.__image_setting)

        self.columnconfigure(self.__gridcolumn_content, weight=1)


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
            input = f"{self.id}:{var_name}"
            input_add(input, InputLabel(self, id=input))
            input_get(input).grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
            self.__input_row_counter += 1


    # get output value that represented by input
    def input_value_get(self, input):
        input = f"{self.id}:{input}"
        result = None

        try:
            result = output_get(input_get(input).text_get()).text_get()
        except:
            pass

        return result


    def output_init(self, *args):
        for var_name in args:
            output = f"{self.id}:{var_name}"
            output_object = OutputLabel(self, id=output)
            output_object.grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
            # output_object.bind('<Double-Button-1>', self.settings)
            output_add(output, output_object)
            self.__output_row_counter += 1


    def output_value_set(self, output, value):
        try:
            output = f"{self.id}:{output}"
            output_get(output).text_set(text=str(value))
        except:
            pass


    def connect(self):
        input_container = input_get_by_plugin(self.id)
        for input_object in input_container:
            input_object.connect()

        output_container = output_get_by_plugin(self.id)
        for output_object in output_container:
            output_object.connect()


    def datalabels_box_set(self):
        input_container = input_get_by_plugin(self.id)
        for input_object in input_container:
            input_object.box_set()

        output_container = output_get_by_plugin(self.id)
        for output_object in output_container:
            output_object.box_set()



class SettingDialog(Dialog):
    def __init__(self, parent, title, name):
        self.plugin_name = name
        super().__init__(parent, title)


    def body(self, frame):
        self.lbl_plugin_name = ttk.Label(frame, width=25, text="Plugin name")
        self.lbl_plugin_name.pack()
        self.ent_plugin_name = ttk.Entry(frame, width=25)
        self.ent_plugin_name.pack()
        self.ent_plugin_name.insert(0, self.plugin_name)

        return frame


    def ok_pressed(self):
        # print("ok")
        self.plugin_name = self.ent_plugin_name.get()
        self.destroy()


    def cancel_pressed(self):
        # print("cancel")
        self.destroy()


    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
