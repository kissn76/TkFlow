import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from datalabel import InputLabel, OutputLabel
import style



# class Pluginbase():
#     '''
#         Pluginbase controller
#     '''
#     pass



# class PluginbaseModel():
#     '''
#         Pluginbase model
#     '''
#     pass



# class PluginbaseView(ttk.Frame):
#     '''
#         Pluginbase view
#     '''
#     pass



class PluginBase(ttk.Frame):
    def __init__(self, master, plugin_id, plugincontainer_id, canvas_object, name=None, parents=[], **kwargs):
        super().__init__(master, **kwargs)
        self.parents = parents
        self.name = name
        self.id = plugin_id
        self.plugincontainer_id = plugincontainer_id
        self.box = ()   # box in canvas
        self.canvas = canvas_object

        self.__input_container = {}
        self.__output_container = {}

        self.__input_row_counter = 0
        self.__output_row_counter = 0
        self.__content_row_counter = 0

        self.__gridcolumn_arranger = 0
        self.__gridcolumn_setting = 1
        self.__gridcoulmn_input = 2
        self.__gridcolumn_content = 3
        self.__gridcolumn_output = 4

        self.__image_setting = ImageTk.PhotoImage(style.image_setting_12)
        self.__image_arranger = ImageTk.PhotoImage(style.image_arranger_12)
        self.__image_move = ImageTk.PhotoImage(style.image_move_12)

        self.columnconfigure(self.__gridcolumn_content, weight=1)

        self.arranger_init()
        self.settings_init()


    def to_dict(self):
        inputs = {}
        for input_object in self.__input_container.values():
            inputs.update(input_object.to_dict())

        outputs = {}
        for output_object in self.__output_container.values():
            outputs.update(output_object.to_dict())

        ret = {self.id: {"inputs": inputs, "outputs": outputs}}
        return ret


    # set box in canvas
    def box_set(self, event=None):
        plugincontainer_box = self.canvas.bbox(f"{self.plugincontainer_id}*plugincontainer")
        plugin_geometry = self.winfo_geometry().replace('x', '+').split("+") # plugin geometry

        x1 = int(plugincontainer_box[0]) + int(plugin_geometry[2])
        y1 = int(plugincontainer_box[1]) + int(plugin_geometry[3])
        x2 = int(x1 + int(plugin_geometry[0]))
        y2 = int(y1 + int(plugin_geometry[1]))

        self.box = (x1, y1, x2, y2)


    def arranger_init(self):
        self.arranger = ttk.Frame(self)
        self.btn_arranger = tk.Button(self.arranger, image=self.__image_move, compound=tk.CENTER)
        self.btn_arranger.grid(row=0, column=0, sticky="nswe")
        self.btn_arranger.bind('<Button-1>', lambda event: self.dnd_arrange_start(event))
        self.btn_arranger.bind('<B1-Motion>', lambda event: self.dnd_arrange_motion(event))
        self.btn_arranger.bind('<ButtonRelease-1>', lambda event: self.dnd_arrange_stop(event))


    def dnd_arrange_start(self, event):
        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()

        self.floating_widget = ttk.Label(self.winfo_toplevel(), text=self.id)
        self.floating_widget.place(x=x, y=y)


    def dnd_arrange_motion(self, event):
        if bool(self.floating_widget):
            x = self.winfo_pointerx() - self.canvas.winfo_rootx()
            y = self.winfo_pointery() - self.canvas.winfo_rooty()

            self.floating_widget.place(x=x, y=y)


    def dnd_arrange_stop(self, event):
        if bool(self.floating_widget):
            self.floating_widget.place_forget()
            self.floating_widget.destroy()

        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)

        box_set_all()
        for obj in get_all().values():
            x1, y1, x2, y2 = obj.box
            # if pointer is in plugin box
            if canvas_x >= x1 and canvas_x <= x2 and canvas_y >= y1 and canvas_y <= y2:
                # if pointer is in beginning of plugin box
                if canvas_y <= int(y1 + ((y2 - y1) / 2)):
                    print(obj.id, "befor")
                # if pointer is in ending of plugin box
                else:
                    print(obj.id, "after")
            else:
                # put plugin in a new widget
                pass


    def settings_init(self):
        self.config = ttk.Frame(self)
        self.btn_config = tk.Button(self.config, image=self.__image_setting, compound=tk.CENTER)
        self.btn_config.grid(row=0, column=0, sticky="nswe")
        self.btn_config.bind('<Button-1>', lambda event: self.settings_open(event))


    def settings_open(self, event):
        print("Settings panel start", type(self), self.id)


    def setting_mode_set(self, setting_mode):
        if not setting_mode:
            self.arranger.grid_remove()
            self.config.grid_remove()
        else:
            self.arranger.grid(row=0, column=self.__gridcolumn_arranger, sticky="nswe")
            self.config.grid(row=0, column=self.__gridcolumn_setting, sticky="nswe")


    def content_init(self, content_object):
        content_object.grid(row=self.__content_row_counter, column=self.__gridcolumn_content, sticky="we")
        self.__content_row_counter += 1


    def input_init(self, *args):
        for var_name in args:
            input_id = f"{self.id}:{var_name}"
            self.__input_container.update({input_id: InputLabel(self, id=input_id, plugin_container_id=self.plugincontainer_id, canvas_object=self.canvas)})
            self.__input_container[input_id].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
            self.__input_row_counter += 1


    # get output value that represented by input
    def input_value_get(self, input):
        input_id = f"{self.id}:{input}"
        result = None
        output_id = self.__input_container[input_id].value_get()
        if bool(output_id):
            plugin_id = output_id.split(':')[0]
            plugin_object = self.canvas.plugin_get(plugin_id)
            result = plugin_object.output_value_get(output_id).value_get()
        return result


    def input_container_get(self):
        return self.__input_container


    def output_init(self, *args):
        for var_name in args:
            output_id = f"{self.id}:{var_name}"
            self.__output_container.update({output_id: OutputLabel(self, id=output_id, plugin_container_id=self.plugincontainer_id, canvas_object=self.canvas)})
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
