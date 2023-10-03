from tkinter import ttk
from PIL import Image, ImageTk
import mainwindow
import pluginbase
import style



class DataLabel(ttk.Frame):
    def __init__(self, master, id, plugin_container_id):
        super().__init__(master)
        self.image_anydata = ImageTk.PhotoImage(style.datatype_any)
        self.image_data = ImageTk.PhotoImage(style.data)

        self.id = id
        self.plugin_container_id = plugin_container_id
        self.box = ()   # box in canvas

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
        plugin_container_box = mainwindow.can_main.bbox(f"{self.plugin_container_id}:plugincontainer")
        plugin_geometry = self.master.winfo_geometry().replace('x', '+').split("+") # plugin geometry
        datalabel_geometry = self.winfo_geometry().replace('x', '+').split("+")     # [width, height, x, y] frame contains icons and value

        x1 = int(plugin_container_box[0]) + int(plugin_geometry[2]) + int(datalabel_geometry[2])
        y1 = int(plugin_container_box[1]) + int(plugin_geometry[3]) + int(datalabel_geometry[3])
        x2 = int(x1 + int(datalabel_geometry[0]))
        y2 = int(y1 + int(datalabel_geometry[1]))

        self.box = (x1, y1, x2, y2)


    def value_set(self, text):
        self.lbl_txt.configure(text=text)


    def value_get(self):
        return self.lbl_txt.cget("text")


    def connect(self, output_object, input_object, line_id=None):
        if not bool(line_id):
            line_id = f"{self.id}:connect_line"

        start_x = output_object.box[2]
        start_y = output_object.box[1] + ((output_object.box[3] - output_object.box[1]) / 2)

        end_x = input_object.box[0]
        end_y = input_object.box[1] + ((input_object.box[3] - input_object.box[1]) / 2)

        # count and draw line
        mainwindow.can_main.connect_line_create(start_x, start_y, end_x, end_y, line_id)


    def diconnect(self, line_id=None):
        if not bool(line_id):
            line_id = f"{self.id}:connect_line"

        mainwindow.can_main.connect_line_delete(line_id)



class InputLabel(DataLabel):
    def __init__(self, master, id, plugin_container_id):
        super().__init__(master, id, plugin_container_id)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")


    def connect(self):
        start_variable_id = self.value_get()
        if bool(start_variable_id):
            plugin_id = start_variable_id.split(':')[0]
            plugin_object = pluginbase.get(plugin_id)
            output_object = plugin_object.output_object_get(start_variable_id)
            super().connect(output_object, self)
        else:
            super().diconnect()



class OutputLabel(DataLabel):
    def __init__(self, master, id, plugin_container_id):
        super().__init__(master, id, plugin_container_id)
        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")

        self.lbl_data.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.bind('<Button-1>', self.dnd_start)
        self.lbl_data.bind('<Button1-Motion>', self.dnd_motion)
        self.lbl_data.bind('<ButtonRelease-1>', self.dnd_stop)


    def dnd_start(self, event):
        self.box_set()


    def dnd_motion(self, event):
        x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
        y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
        canvas_x = mainwindow.can_main.canvasx(x)
        canvas_y = mainwindow.can_main.canvasy(y)

        start_x = self.box[2]
        start_y = self.box[1] + ((self.box[3] - self.box[1]) / 2)

        mainwindow.can_main.connect_line_create(start_x, start_y, canvas_x, canvas_y, "drawing")

        input_object = self.input_object_find(canvas_x, canvas_y)
        if bool(input_object):
            print("m", input_object.id)
            input_object.enter()


    def dnd_stop(self, event):
        mainwindow.can_main.connect_line_delete("drawing")

        input_object = self.input_object_find()
        if bool(input_object):
            input_object.value_set(self.id)
            input_object.connect()


    def input_object_find(self, canvas_x=None, canvas_y=None):
        ret = None

        if not bool(canvas_x) or not bool(canvas_y):
            x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
            y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
            canvas_x = mainwindow.can_main.canvasx(x)
            canvas_y = mainwindow.can_main.canvasy(y)
        else:
            print(canvas_x, canvas_y)

        can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, mainwindow.can_main.cget("scrollregion").split()))
        if canvas_x > 0 and canvas_y > 0 and canvas_x < can_main_width and canvas_y < can_main_height:
            try:
                widgets = mainwindow.can_main.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)

                if len(widgets) > 0:
                    widget_tags = set()
                    for id in widgets:
                        tags = mainwindow.can_main.gettags(id)
                        if len(tags) > 0:
                            widget_id, widget_type = tags[0].split(':')

                            if widget_type == "plugincontainer":
                                widget_tags.add(tags[0])

                    if len(widget_tags) == 1:
                        target_widget_tag = list(widget_tags)[0].split(':')[0]
                        input_object_list = []
                        for plugin_object in pluginbase.get_all().values():
                            if plugin_object.plugin_container_id == target_widget_tag:
                                for input_object in plugin_object.input_container_get().values():
                                    input_object_list.append(input_object)
                        for input_object in input_object_list:
                            if canvas_x >= input_object.box[0] and canvas_x <= input_object.box[2] and canvas_y >= input_object.box[1] and canvas_y <= input_object.box[3]:
                                ret = input_object
                                break
                    else:
                        print("too many widget are overlapped:", widget_tags)
            except:
                pass

        return ret


    def connect(self):
        for plugin_object in pluginbase.get_all().values():
            for input_object in plugin_object.input_container_get().values():
                if input_object.value_get() == self.id:
                    line_id = f"{input_object.id}:connect_line"
                    super().connect(self, input_object, line_id)
