from tkinter import ttk
from PIL import Image, ImageTk
import mainwindow



clipboard = None


__input_container = {}
__output_container = {}


# get input objects by variable_id (widget_id:plugin_id:variable_id)
def input_get(input_variable_id):
    object = None
    try:
        object = __input_container[input_variable_id]
    except:
        pass
    return object


# get input objects in a list filtered by plugin_id (widget_id:plugin_id)
def input_get_by_plugin(plugin_id):
    objects = []
    for input_key, input_object in __input_container.items():
        if input_key.startswith(plugin_id):
            objects.append(input_object)

    return objects


# add input object
def input_add(variable_id, object):
    __input_container.update({variable_id: object})


# get input objects in a list filtered by object connect to output object variable
def input_get_by_output(output_variable_id):
    objects = []
    for input_key, input_object in __input_container.items():
        if input_object.text_get() == output_variable_id:
            objects.append(input_object)

    return objects


def output_get(name):
    object = None
    try:
        object = __output_container[name]
    except:
        pass
    return object


def output_get_by_plugin(plugin_id):
    objects = []
    for output_key, output_object in __output_container.items():
        if output_key.startswith(plugin_id):
            objects.append(output_object)

    return objects


def output_add(name, object):
    __output_container.update({name: object})



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


    # copy plugin id to clipboard
    def copy(self, event):
        global clipboard
        clipboard = self.id


    # paste plugin id from clipboard
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


    def connect(self, output_object, input_object, tags):
        # output object where line starts
        start_plugin_container_box = mainwindow.can_main.bbox(f"{output_object.id.split(':')[0]}:plugincontainer")
        start_plugin_geometry = output_object.lbl_data.master.master.winfo_geometry().replace('x', '+').split("+")  # plugin geometry
        start_rowframe_geometry = output_object.lbl_data.master.winfo_geometry().replace('x', '+').split("+")   # [width, height, x, y] frame contains icons and value

        start_x = int(start_plugin_container_box[2])
        start_y = int(start_plugin_container_box[1]) + int(start_plugin_geometry[3]) + int(start_rowframe_geometry[3]) + int(int(start_rowframe_geometry[1]) / 2)

        # input object where line ends
        end_plugin_container_box = mainwindow.can_main.bbox(f"{input_object.id.split(':')[0]}:plugincontainer")
        end_plugin_geometry = input_object.lbl_data.master.master.winfo_geometry().replace('x', '+').split("+")  # plugin geometry
        end_rowframe_geometry = input_object.lbl_data.master.winfo_geometry().replace('x', '+').split("+")   # [width, height, x, y] frame contains icons and value

        end_x = int(end_plugin_container_box[0])
        end_y = int(end_plugin_container_box[1]) + int(end_plugin_geometry[3]) + int(end_rowframe_geometry[3]) + int(int(end_rowframe_geometry[1]) / 2)

        # count and draw line
        self.draw_connect(start_x, start_y, end_x, end_y, tags)


    def draw_connect(self, start_x, start_y, end_x, end_y, tags):
        offset = (end_x - start_x) / 3
        mid_0_x = start_x + offset
        mid_0_y = start_y
        mid_1_x = end_x - offset
        mid_1_y = end_y

        mainwindow.can_main.create_line(
                start_x, start_y,
                mid_0_x, mid_0_y,
                mid_1_x, mid_1_y,
                end_x, end_y,
                smooth=True, tags=tags
            )



class InputLabel(DataLabel):
    def __init__(self, master, id=None):
        super().__init__(master, id=id)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data.bind('<Double-Button-1>', self.paste)

        # self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        # self.lbl_data_type.bind('<Double-Button-1>', self.paste)

        self.output_input_line = None


    def paste(self, event):
        super().paste(event)
        self.connect()


    def connect(self):
        start_variable_id = self.text_get()
        try:
            if bool(self.output_input_line):
                mainwindow.can_main.delete(self.output_input_line)
            self.output_input_line = f"{start_variable_id}-{self.id}"
            output_object = output_get(start_variable_id)

            super().connect(output_object, self, self.output_input_line)
        except:
            pass



class OutputLabel(DataLabel):
    def __init__(self, master, id=None):
        super().__init__(master, id=id)
        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")
        # self.lbl_txt.bind('<Double-Button-1>', self.copy)

        # self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        # self.lbl_data_type.bind('<Double-Button-1>', self.copy)

        self.lbl_data.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.bind('<Double-Button-1>', self.copy)
        self.lbl_data.bind('<Button-1>', self.dnd_start)
        self.lbl_data.bind('<Button1-Motion>', self.dnd_motion)
        self.lbl_data.bind('<ButtonRelease-1>', self.dnd_stop)


    def dnd_start(self, event):
        print("Output dnd start")


    def dnd_motion(self, event):
        start_plugin_container_box = mainwindow.can_main.bbox(f"{self.id.split(':')[0]}:plugincontainer")
        start_plugin_geometry = self.lbl_data.master.master.winfo_geometry().replace('x', '+').split("+")  # plugin geometry
        start_rowframe_geometry = self.lbl_data.master.winfo_geometry().replace('x', '+').split("+")   # [width, height, x, y] frame contains icons and value

        start_x = int(start_plugin_container_box[2])
        start_y = int(start_plugin_container_box[1]) + int(start_plugin_geometry[3]) + int(start_rowframe_geometry[3]) + int(int(start_rowframe_geometry[1]) / 2)

        mainwindow.can_main.delete("drawing")
        self.draw_connect(start_x, start_y, mainwindow.can_main.canvasx(event.x), mainwindow.can_main.canvasy(event.y), "drawing")


    def dnd_stop(self, event):
        mainwindow.can_main.delete("drawing")


    def connect(self):
        start_variable_id = self.id
        try:
            for input_object in input_get_by_output(start_variable_id):
                line_id = f"{start_variable_id}-{input_object.id}"
                mainwindow.can_main.delete(line_id)

                super().connect(self, input_object, line_id)
        except Exception as e:
            print(e)
