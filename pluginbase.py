import tkinter as tk
from tkinter.simpledialog import Dialog
from tkinter import ttk
from PIL import Image, ImageTk
import mainwindow



clipboard = None

__input_container = {}
__output_container = {}


def input_get(name):
    object = None
    try:
        object = __input_container[name]
    except:
        pass
    return object


def input_add(name, object):
    __input_container.update({name: object})


def output_get(name):
    object = None
    try:
        object = __output_container[name]
    except:
        pass
    return object


def output_add(name, object):
    __output_container.update({name: object})



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



class DataLabel(ttk.Frame):
    def __init__(self, master, id=None):
        super().__init__(master)
        MAX_SIZE = (12, 12)
        datatype_any = Image.open(f"./resources/icon/anydata.png")
        data = Image.open(f"./resources/icon/arrow_right.png")
        datatype_any.thumbnail(MAX_SIZE)
        data.thumbnail(MAX_SIZE)
        self.image_anydata = ImageTk.PhotoImage(datatype_any)
        self.image_data = ImageTk.PhotoImage(data)

        self.id = id

        self.lbl_txt = ttk.Label(self, text="a")
        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        # self.lbl_data.bind("<Button-1>", lambda event: self.dnd_start(event))
        # self.lbl_data.bind('<B1-Motion>', lambda event: self.dnd_motion(event))


    def copy(self, event):
        global clipboard
        clipboard = self.id


    def paste(self, event):
        global clipboard
        self.text_set(clipboard)


    def text_set(self, text):
        self.lbl_txt.configure(text=text)


    def text_get(self):
        return self.lbl_txt.cget("text")


    def dnd_start(self, event):
        pass


    def dnd_motion(self, event):
        pass



class InputLabel(DataLabel):
    def __init__(self, master, id=None):
        super().__init__(master, id=id)
        # self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.grid(row=0, column=2, sticky="n, s, w, e")

        # self.lbl_txt.bind('<Double-Button-1>', self.copy)
        self.lbl_data_type.bind('<Double-Button-1>', self.paste)
        self.lbl_data.bind('<Double-Button-1>', self.paste)
        # self.lbl_data.bind('<B1-Motion>', self.connect)


    def paste(self, event):
        super().paste(event)
        self.connect(event=event)


    def connect(self, event):
        # output_object = output_get(self.text_get())

        widget, plugin, variable = self.text_get().split(':')
        start_id = f"{widget}:{plugin}:plugin"
        start_plugin_container_position = mainwindow.can_main.coords(start_id)
        start_plugin_box = mainwindow.can_main.bbox(start_id)

        widget, plugin, variable = self.id.split(':')
        end_id = f"{widget}:{plugin}:plugin"
        end_plugin_container_position = mainwindow.can_main.coords(end_id)
        end_plugin_box = mainwindow.can_main.bbox(end_id)

        print(start_id, start_plugin_container_position, start_plugin_box)
        print(end_id, end_plugin_container_position, end_plugin_box)

        # plugin_container_width = output_object.lbl_data.master.master.master.winfo_width()
        # plugin_container_height = output_object.lbl_data.master.master.master.winfo_height()

        # print(output_object.lbl_data, output_object.lbl_data.winfo_reqheight())
        # print(output_object.lbl_data.master, output_object.lbl_data.master.winfo_height())
        # print(output_object.lbl_data.master.master, output_object.lbl_data.master.master.winfo_height())
        # print(output_object.lbl_data.master.master.master, output_object.lbl_data.master.master.master.winfo_height())
        # print(output_object.lbl_data.master.master.master.master, output_object.lbl_data.master.master.master.master.winfo_height())

        print(self.lbl_data, self.lbl_data.winfo_geometry())
        print(self.lbl_data.master, self.lbl_data.master.winfo_geometry())
        print(self.lbl_data.master.master, self.lbl_data.master.master.winfo_geometry())
        print(self.lbl_data.master.master.master, self.lbl_data.master.master.master.winfo_geometry())
        print(self.lbl_data.master.master.master.master, self.lbl_data.master.master.master.master.winfo_geometry())

        # start_x = plugin_container_position[0] + plugin_container_width
        # start_y = plugin_container_position[1] + plugin_container_height / 2

        # widget, plugin, variable = self.id.split(':')
        # id = f"{widget}:{plugin}:plugin"
        # plugin_container_position = mainwindow.can_main.coords(id)
        # plugin_container_height = self.lbl_data.master.master.master.winfo_height()

        # end_x = plugin_container_position[0]
        # end_y = plugin_container_position[1] + plugin_container_height / 2

        # mainwindow.can_main.create_line(start_x, start_y, end_x, end_y, smooth=True)

        # s_x = output_object.lbl_data.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
        # s_y = output_object.lbl_data.winfo_rooty() - self.winfo_toplevel().winfo_rooty()
        # start_x = mainwindow.can_main.canvasx(s_x)
        # start_y = mainwindow.can_main.canvasy(s_y)

        # print(
        #     (output_object.lbl_data.winfo_rootx(), output_object.lbl_data.winfo_rooty()),
        #     (s_x, s_y),
        #     (start_x, start_y),
        #     (mainwindow.can_main.canvasx(mainwindow.can_main.winfo_width()), mainwindow.can_main.canvasy(mainwindow.can_main.winfo_height()))
        #     )

        # e_x = self.lbl_data.winfo_rootx() - self.winfo_toplevel().winfo_rootx()
        # e_y = self.lbl_data.winfo_rooty() - self.winfo_toplevel().winfo_rooty()
        # end_x = mainwindow.can_main.canvasx(e_x)
        # end_y = mainwindow.can_main.canvasy(e_y)

        # print(
        #     (self.lbl_data.winfo_x(), self.winfo_y()),
        #     (self.lbl_data.pare().winfo_parent(), self.lbl_data.winfo_parent()),
        #     (self.lbl_data.winfo_rootx(), self.lbl_data.winfo_rooty()),
        #     )


        # offset = (end_x - start_x) / 3

        # mid_0_x = start_x + offset
        # mid_0_y = start_y

        # mid_1_x = end_x - offset
        # mid_1_y = end_y
        # mainwindow.can_main.create_line(start_x,start_y, mid_0_x,mid_0_y, mid_1_x,mid_1_y, end_x,end_y, smooth=True)



class OutputLabel(DataLabel):
    def __init__(self, master, id=None):
        super().__init__(master, id=id)
        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.grid(row=0, column=2, sticky="n, s, w, e")

        self.lbl_txt.bind('<Double-Button-1>', self.copy)
        self.lbl_data_type.bind('<Double-Button-1>', self.copy)
        self.lbl_data.bind('<Double-Button-1>', self.copy)
