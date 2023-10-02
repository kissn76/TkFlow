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

        # self.lbl_data.bind("<Button-1>", lambda event: self.position_set(event))
        # self.lbl_data.bind('<B1-Motion>', lambda event: self.dnd_motion(event))


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


    def connect(self, output_object, input_object, tags):
        start_x = output_object.box[2]
        start_y = output_object.box[1] + ((output_object.box[3] - output_object.box[1]) / 2)

        end_x = input_object.box[0]
        end_y = input_object.box[1] + ((input_object.box[3] - input_object.box[1]) / 2)

        # count and draw line
        self.draw_connect(start_x, start_y, end_x, end_y, tags)


    def draw_connect(self, start_x, start_y, end_x, end_y, tags):
        offset = (end_x - start_x) / 3
        mid_0_x = start_x + offset
        mid_0_y = start_y
        mid_1_x = end_x - offset
        mid_1_y = end_y

        line_id = mainwindow.can_main.create_line(
                start_x, start_y,
                mid_0_x, mid_0_y,
                mid_1_x, mid_1_y,
                end_x, end_y,
                smooth=True, tags=tags
            )

        mainwindow.can_main.tag_bind(line_id, "<Button-1>", lambda event: mainwindow.can_main.itemconfigure(line_id, fill="red"))



class InputLabel(DataLabel):
    def __init__(self, master, id, plugin_container_id):
        super().__init__(master, id, plugin_container_id)
        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")

        # self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")

        self.output_input_line = None


    def connect(self):
        start_variable_id = self.value_get()
        if bool(start_variable_id):
            if bool(self.output_input_line):
                mainwindow.can_main.delete(self.output_input_line)
            self.output_input_line = f"{start_variable_id}-{self.id}"

            for plugin_object in pluginbase.get_all().values():
                for output_object in plugin_object.output_container_get().values():
                    if output_object.id == start_variable_id:
                        super().connect(output_object, self, self.output_input_line)
                        return



class OutputLabel(DataLabel):
    def __init__(self, master, id, plugin_container_id):
        super().__init__(master, id, plugin_container_id)
        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")

        # self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")

        self.lbl_data.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.bind('<Button-1>', self.dnd_start)
        self.lbl_data.bind('<Button1-Motion>', self.dnd_motion)
        self.lbl_data.bind('<ButtonRelease-1>', self.dnd_stop)
        self.lbl_data.bind("<Enter>", self.enter)
        self.lbl_data.bind("<Leave>", self.leave)

        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TLabel', background='#334353')


    def enter(self, event):
        self.lbl_data.configure(style="My.TLabel")


    def leave(self, event):
        self.lbl_data.configure(style="")


    def dnd_start(self, event):
        self.box_set()


    def dnd_motion(self, event):
        x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
        y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
        canvas_x = mainwindow.can_main.canvasx(x)
        canvas_y = mainwindow.can_main.canvasy(y)

        start_x = self.box[2]
        start_y = self.box[1] + ((self.box[3] - self.box[1]) / 2)

        mainwindow.can_main.delete("drawing")
        self.draw_connect(start_x, start_y, canvas_x, canvas_y, "drawing")


    def dnd_stop(self, event):
        mainwindow.can_main.delete("drawing")

        x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
        y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
        canvas_x = mainwindow.can_main.canvasx(x)
        canvas_y = mainwindow.can_main.canvasy(y)

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
                            for input_object in plugin_object.input_container_get().values():
                                if input_object.plugin_container_id == target_widget_tag:
                                    input_object_list.append(input_object)
                        for input_object in input_object_list:
                            if canvas_x >= input_object.box[0] and canvas_x <= input_object.box[2] and canvas_y >= input_object.box[1] and canvas_y <= input_object.box[3]:
                                input_object.value_set(self.id)
                                input_object.connect()
                                break
                    else:
                        print("too many widget are overlapped:", widget_tags)
            except:
                pass



    def connect(self):
        for plugin_object in pluginbase.get_all().values():
            for input_object in plugin_object.input_container_get().values():
                if input_object.value_get() == self.id:
                    line_id = f"{self.id}-{input_object.id}"
                    mainwindow.can_main.delete(line_id)
                    super().connect(self, input_object, line_id)
