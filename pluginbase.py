import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from datalabel import InputLabel, OutputLabel, input_add, input_get, input_get_by_plugin, output_add, output_get, output_get_by_plugin



class PluginBase(ttk.Frame):
    def __init__(self, master, id):
        super().__init__(master)
        self.name = id
        self.id = id

        self.input_row_counter = 0
        self.output_row_counter = 0

        self.columnconfigure(1, weight=1)
        self.bind('<Button-3>', self.settings)


    def settings(self, event):
        print(type(self), self.id)


    def input_init(self, *args):
        for var_name in args:
            input = f"{self.id}:{var_name}"
            input_add(input, InputLabel(self, id=input))
            input_get(input).grid(row=self.input_row_counter, column=0)
            self.input_row_counter += 1


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
            output_object.grid(row=self.output_row_counter, column=3)
            # output_object.bind('<Double-Button-1>', self.settings)
            output_add(output, output_object)
            self.output_row_counter += 1


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
