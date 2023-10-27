from tkinter import ttk
from PIL import ImageTk
import style



class DataLabel(ttk.Frame):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master)
        self.image_anydata = ImageTk.PhotoImage(style.image_datatype_any_12)
        self.image_data = ImageTk.PhotoImage(style.image_data_12)

        self.__id = id
        self.__plugin_id = plugin_id
        self.pluginframe_id = pluginframe_id
        self.__box = ()   # box in canvas
        self.canvas = canvas_object

        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TLabel', background='#334353')

        self.lbl_data.bind("<Enter>", self.enter)
        self.lbl_data.bind("<Leave>", self.leave)


    def id_get(self):
        return self.__id


    def plugin_id_get(self):
        return self.__plugin_id


    def enter(self, event=None):
        self.lbl_data.configure(style="My.TLabel")


    def leave(self, event=None):
        self.lbl_data.configure(style="")


    def to_dict(self):
        ret = {self.__id: {"value": self.value_get()}}
        return ret


    # set box in canvas
    def box_set(self, event=None):
        pluginframe_box = self.canvas.bbox(f"{self.pluginframe_id}*pluginframe")
        plugin_geometry = self.master.winfo_geometry().replace('x', '+').split("+") # plugin geometry
        datalabel_geometry = self.winfo_geometry().replace('x', '+').split("+")     # [width, height, x, y] frame contains icons and value

        x1 = int(pluginframe_box[0]) + int(plugin_geometry[2]) + int(datalabel_geometry[2])
        y1 = int(pluginframe_box[1]) + int(plugin_geometry[3]) + int(datalabel_geometry[3])
        x2 = int(x1 + int(datalabel_geometry[0]))
        y2 = int(y1 + int(datalabel_geometry[1]))

        self.__box = (x1, y1, x2, y2)


    def box_get(self):
        return self.__box



class InputLabel(DataLabel):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master, id, plugin_id, pluginframe_id, canvas_object)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")



class OutputLabel(DataLabel):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master, id, plugin_id, pluginframe_id, canvas_object)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data.bind('<Button-1>', self.dnd_start)
        self.lbl_data.bind('<Button1-Motion>', self.dnd_motion)
        self.lbl_data.bind('<ButtonRelease-1>', self.dnd_stop)

        self.__last_input_object = None


    def dnd_start(self, event):
        pass


    def dnd_motion(self, event):
        display_x, display_y, canvas_x, canvas_y = self.canvas.cursor_position_get()

        # draw line between outputlabel and pointer
        start_box = self.box_get()
        start_x = start_box[2]
        start_y = start_box[1] + ((start_box[3] - start_box[1]) / 2)

        self.canvas.connect_line_create(start_x, start_y, canvas_x, canvas_y, "drawing")

        # enter/leave inputlabel
        if bool(self.__last_input_object):
            self.__last_input_object.leave()
            self.__last_input_object = None

        input_objects = self.canvas.cursor_inputlabel_find()
        if bool(input_objects):
            input_object = input_objects[0]
            input_object.enter()
            self.__last_input_object = input_object


    def dnd_stop(self, event):
        self.canvas.connect_line_delete("drawing")
        self.__last_input_object = None

        input_objects = self.canvas.cursor_inputlabel_find()    # find inputlabel under cursor position
        if bool(input_objects):
            input_object = input_objects[0]
            new_value = f"{self.plugin_id_get()}:{self.id_get()}"
            old_value = self.canvas.plugin_input_value_get(input_object.plugin_id_get(), input_object.id_get()) # get old value of found inputlabel

            if not old_value == new_value:  # if value modified
                if bool(old_value): # if found inputlabel is not empty
                    # delete old line
                    self.canvas.disconnect(old_value, f"{input_object.plugin_id_get()}:{input_object.id_get()}")
                # insert new value, create new line
                self.canvas.plugin_input_value_set(input_object.plugin_id_get(), input_object.id_get(), new_value)
                self.canvas.connect(f"{self.plugin_id_get()}:{self.id_get()}", f"{input_object.plugin_id_get()}:{input_object.id_get()}")
