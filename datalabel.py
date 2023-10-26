from tkinter import ttk
from PIL import ImageTk
import style



class DataLabel(ttk.Frame):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master)
        self.image_anydata = ImageTk.PhotoImage(style.image_datatype_any_12)
        self.image_data = ImageTk.PhotoImage(style.image_data_12)

        self.id = id
        self.plugin_id = plugin_id
        self.pluginframe_id = pluginframe_id
        self.box = ()   # box in canvas
        self.canvas = canvas_object

        self.lbl_txt = ttk.Label(self, text="")
        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TLabel', background='#334353')

        self.lbl_data.bind("<Enter>", self.enter)
        self.lbl_data.bind("<Leave>", self.leave)


    def enter(self, event=None):
        self.lbl_data.configure(style="My.TLabel")


    def leave(self, event=None):
        self.lbl_data.configure(style="")


    def to_dict(self):
        ret = {self.id: {"value": self.value_get()}}
        return ret


    # set box in canvas
    def box_set(self, event=None):
        plugin_container_box = self.canvas.bbox(f"{self.pluginframe_id}*pluginframe")
        plugin_geometry = self.master.winfo_geometry().replace('x', '+').split("+") # plugin geometry
        datalabel_geometry = self.winfo_geometry().replace('x', '+').split("+")     # [width, height, x, y] frame contains icons and value

        x1 = int(plugin_container_box[0]) + int(plugin_geometry[2]) + int(datalabel_geometry[2])
        y1 = int(plugin_container_box[1]) + int(plugin_geometry[3]) + int(datalabel_geometry[3])
        x2 = int(x1 + int(datalabel_geometry[0]))
        y2 = int(y1 + int(datalabel_geometry[1]))

        self.box = (x1, y1, x2, y2)


    def value_set(self, text):
        if text == None:
            text = ""
        self.lbl_txt.configure(text=str(text))


    def value_get(self):
        return self.lbl_txt.cget("text")


    def connect(self, output_object, input_object, line_id=None):
        if not bool(line_id):
            line_id = f"{self.plugin_id}:{self.id}*connect_line"

        start_x = output_object.box[2]
        start_y = output_object.box[1] + ((output_object.box[3] - output_object.box[1]) / 2)

        end_x = input_object.box[0]
        end_y = input_object.box[1] + ((input_object.box[3] - input_object.box[1]) / 2)

        # count and draw line
        self.canvas.connect_line_create(start_x, start_y, end_x, end_y, line_id)


    def disconnect(self, line_id=None):
        if not bool(line_id):
            line_id = f"{self.id}*connect_line"

        self.canvas.connect_line_delete(line_id)



class InputLabel(DataLabel):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master, id, plugin_id, pluginframe_id, canvas_object)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")


    def connect(self):
        start_variable_id = self.value_get()
        if bool(start_variable_id):
            plugin_id, output_id = start_variable_id.split(':')
            plugin_object = self.canvas.plugin_get(plugin_id)
            output_object = plugin_object.output_object_get(output_id)
            super().connect(output_object, self)
        else:
            super().disconnect()



class OutputLabel(DataLabel):
    def __init__(self, master, id, plugin_id, pluginframe_id, canvas_object):
        super().__init__(master, id, plugin_id, pluginframe_id, canvas_object)
        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")

        self.lbl_data.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.bind('<Button-1>', self.dnd_start)
        self.lbl_data.bind('<Button1-Motion>', self.dnd_motion)
        self.lbl_data.bind('<ButtonRelease-1>', self.dnd_stop)

        self.__last_input_object = None


    def dnd_start(self, event):
        self.box_set()


    def dnd_motion(self, event):
        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)

        start_x = self.box[2]
        start_y = self.box[1] + ((self.box[3] - self.box[1]) / 2)

        self.canvas.connect_line_create(start_x, start_y, canvas_x, canvas_y, "drawing")

        if bool(self.__last_input_object):
            self.__last_input_object.leave()
            self.__last_input_object = None

        input_object = self.input_object_find()
        if bool(input_object):
            input_object.enter()
            self.__last_input_object = input_object


    def dnd_stop(self, event):
        self.canvas.connect_line_delete("drawing")
        self.__last_input_object = None

        input_object = self.input_object_find()
        if bool(input_object):
            plugin_object = self.canvas.plugin_get(input_object.plugin_id)
            plugin_object.input_value_set(input_object.id, f"{self.plugin_id}:{self.id}")
            input_object.connect()


    def input_object_find(self) -> InputLabel:
        ret = None

        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)

        can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, self.canvas.cget("scrollregion").split()))
        if canvas_x > 0 and canvas_y > 0 and canvas_x < can_main_width and canvas_y < can_main_height:
            widgets = self.canvas.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)

            if len(widgets) > 0:
                widget_tags = []
                for id in widgets:
                    tags = self.canvas.gettags(id)
                    if len(tags) > 0:
                        widget_unpack = tags[0].split('*')
                        if len(widget_unpack) > 1:
                            if widget_unpack[1] == "pluginframe":
                                widget_tags.append(tags[0])

                widget_tags = list(set(widget_tags))

                if len(widget_tags) == 1:
                    target_widget_tag = widget_tags[0].split('*')[0]
                    input_object_list = []
                    pluginframe = self.canvas.pluginframe_get(target_widget_tag)
                    for plugin_object in pluginframe.pluginview_get().values():
                        for input_object in plugin_object.input_container_get().values():
                            input_object_list.append(input_object)
                    for input_object in input_object_list:
                        if canvas_x >= input_object.box[0] and canvas_x <= input_object.box[2] and canvas_y >= input_object.box[1] and canvas_y <= input_object.box[3]:
                            ret = input_object
                            break

        return ret


    def connect(self):
        for plugin_object in self.canvas.plugin_get().values():
            for input_id, input_value in plugin_object.input_value_get().items():
                if bool(input_value):
                    if input_value == f"{self.plugin_id}:{self.id}":
                        line_id = f"{plugin_object.id_get()}:{input_id}*connect_line"
                        super().connect(self, plugin_object.input_object_get(input_id), line_id)
