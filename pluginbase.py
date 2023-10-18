import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from datalabel import InputLabel, OutputLabel
import style
# import maincanvas
import plugincontainer



class Pluginbase():
    '''
        Pluginbase controller
    '''
    def __init__(self, master, plugin_id, plugincontainer_id, canvas_object, **kwargs):
        self.view = None
        self.model = PluginbaseModel(plugin_id, plugincontainer_id)
        self.canvas = canvas_object

        self.view_create(master, canvas_object, **kwargs)


    def id_get(self):
        return self.model.id


    def view_create(self, master, canvas_object, **kwargs):
        try:
            self.view.destroy()
        except:
            pass
        self.view = None
        self.view = PluginbaseView(master, canvas_object, self.model, **kwargs)


    def input_init(self, *args):
        for var_name in args:
            self.view.input_init(var_name)
            self.input_value_set(var_name, None)


    def input_value_set(self, input, value):
        self.model.input_value_set(input, value)
        self.view.input_value_set(input)


    def input_value_get(self, input):
        input_id = f"{self.model.id}:{input}"
        return self.model.input_value_get(input_id)


    # get output value that represented by input
    def input_reference_get(self, input):
        input_id = f"{self.model.id}:{input}"
        result = None
        output_id = self.model.input_value_get(input)
        if bool(output_id):
            plugin_id = output_id.split(':')[0]
            plugin_object = self.view.canvas.plugin_get(plugin_id)
            result = plugin_object.output_value_get(output_id)
        return result


    def input_value_get_all(self):
        return self.model.input_value_get_all()


    def output_init(self, *args):
        for var_name in args:
            self.view.output_init(var_name)
            self.output_value_set(var_name, "")


    def output_value_set(self, output, value):
        self.model.output_value_set(output, value)
        self.view.output_value_set(output)


    def output_value_get(self, output):
        return self.model.output_value_get(output)


    def content_init(self, content_object):
        self.view.content_init(content_object)



class PluginbaseModel():
    '''
        Pluginbase model
    '''
    def __init__(self, plugin_id, plugincontainer_id):
        self.id = plugin_id
        self.plugincontainer_id = plugincontainer_id

        self.__input_value_container = {}
        self.__output_value_container = {}


    def input_value_set(self, input, value):
        self.__input_value_container[input] = value


    def input_value_get(self, input):
        return self.__input_value_container[input]


    def input_value_get_all(self):
        return self.__input_value_container.copy()


    def output_value_set(self, output, value):
        self.__output_value_container[output] = value


    def output_value_get(self, output):
        return self.__output_value_container[output]



class PluginbaseView(ttk.Frame):
    '''
        Pluginbase view
    '''
    def __init__(self, master: plugincontainer.Plugincontainer, canvas_object, model: PluginbaseModel, **kwargs):
        super().__init__(master, **kwargs)
        self.model = model
        self.box = ()   # box in canvas
        self.canvas = canvas_object
        self.plugincontainer = master

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

        ret = {self.model.id: {"inputs": inputs, "outputs": outputs}}
        return ret


    # set box in canvas
    def box_set(self, event=None):
        plugincontainer_box = self.canvas.bbox(f"{self.plugincontainer.id}*plugincontainer")
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
        print("Settings panel start", type(self), self.model.id)


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


    def input_init(self, input_id):
        self.__input_container.update({input_id: InputLabel(self, id=input_id, plugin_container_id=self.plugincontainer.id, canvas_object=self.canvas)})
        self.__input_container[input_id].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
        self.__input_row_counter += 1


    def input_value_set(self, input):
        self.__input_container[input].value_set(text=self.model.input_value_get(input))


    def output_init(self, output_id):
        self.__output_container.update({output_id: OutputLabel(self, id=output_id, plugin_container_id=self.plugincontainer.id, canvas_object=self.canvas)})
        self.__output_container[output_id].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
        self.__output_row_counter += 1


    def output_value_set(self, output):
        text = self.model.output_value_get(output)
        self.__output_container[output].value_set(text=text)


    def input_container_get(self):
        return self.__input_container


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
