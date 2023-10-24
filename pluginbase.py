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
    def __init__(self, plugin_id, plugincontainer_object, canvas_object, **kwargs):
        self.__view = None
        self.__model = PluginbaseModel(plugin_id)
        self.__canvas = canvas_object

        self.view_create(plugincontainer_object)


    def id_get(self):
        return self.__model.id_get()


    def view_create(self, plugincontainer_object, **kwargs):
        self.__view = PluginbaseView(plugincontainer_object, self.__canvas, self.__model, **kwargs)
        self.__view.setting_mode_set(plugincontainer_object.setting_mode_get())


    def view_init(self):
        for var_name in self.input_value_get().keys():
            self.__view.input_init(var_name)

        for var_name in self.output_value_get().keys():
            self.__view.output_init(var_name)


    def view_get(self):
        return self.__view


    def input_init(self, *args):
        for var_name in args:
            self.__model.input_value_set(var_name, None)


    def input_object_get(self, input):
        return self.__view.input_object_get(input)


    def input_value_set(self, input, value):
        self.__model.input_value_set(input, value)
        self.__view.input_value_set(input)


    def input_value_get(self, input=None):
        ret = None
        if input == None:
            ret = self.__model.input_value_get_all()
        else:
            ret = self.__model.input_value_get(input)
        return ret


    # get output value that represented by input
    def input_value_get_referenced(self, input):
        result = None
        input_value = self.__model.input_value_get(input)
        if bool(input_value):
            plugin_id, output_id  = input_value.split(':')
            plugin_object = self.__canvas.plugin_get(plugin_id)
            result = plugin_object.output_value_get(output_id)
        return result


    def output_init(self, *args):
        for var_name in args:
            self.__model.output_value_set(var_name, None)


    def output_object_get(self, output):
        return self.__view.output_object_get(output)


    def output_value_set(self, output, value):
        self.__model.output_value_set(output, value)
        self.__view.output_value_set(output)


    def output_value_get(self, output=None):
        ret = None
        if output == None:
            ret = self.__model.output_value_get_all()
        else:
            ret = self.__model.output_value_get(output)
        return ret


    def content_init(self, content_object):
        self.__view.content_init(content_object)



class PluginbaseModel():
    '''
        Pluginbase model
    '''
    def __init__(self, plugin_id):
        self.__id = plugin_id

        self.__input_value_container = {}
        self.__output_value_container = {}


    def id_get(self):
        return self.__id


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


    def output_value_get_all(self):
        return self.__output_value_container.copy()



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

        self.floating_widget = None
        self.marker_widget = None

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

        self.bind('<Enter>', lambda event: self.enter(event))
        self.bind('<Leave>', lambda event: self.leave())


    def enter(self, event):
        self.leave()
        self.box_set()
        self.marker_widget = ttk.Label(self.winfo_toplevel(), text=f"{self.plugincontainer.id_get()}-{self.model.id_get()}")
        x = self.box[2]
        y = self.box[1]
        self.marker_widget.place(x=x, y=y)


    def leave(self):
        if bool(self.marker_widget):
            self.marker_widget.place_forget()
            self.marker_widget.destroy()
            self.marker_widget = None


    def to_dict(self):
        inputs = {}
        for input_object in self.__input_container.values():
            inputs.update(input_object.to_dict())

        outputs = {}
        for output_object in self.__output_container.values():
            outputs.update(output_object.to_dict())

        ret = {self.model.id_get(): {"inputs": inputs, "outputs": outputs}}
        return ret


    # set box in canvas
    def box_set(self, event=None):
        plugincontainer_box = self.canvas.bbox(f"{self.plugincontainer.id_get()}*plugincontainer")
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
        self.leave()
        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()

        self.floating_widget = ttk.Label(self.winfo_toplevel(), text=self.model.id_get())
        self.floating_widget.place(x=x, y=y)


    def dnd_arrange_motion(self, event):
        if bool(self.floating_widget):
            x = self.winfo_pointerx() - self.canvas.winfo_rootx()
            y = self.winfo_pointery() - self.canvas.winfo_rooty()

            self.floating_widget.place(x=x, y=y)


    def dnd_arrange_stop(self, event):
        plugin_id_move = self.floating_widget.cget("text")
        if bool(self.floating_widget):
            self.floating_widget.place_forget()
            self.floating_widget.destroy()
            self.floating_widget = None

        x = self.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.winfo_pointery() - self.canvas.winfo_rooty()
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)

        # pointer pozíció:
        #   - ugyanazon plugincontainer
        #       - ugyanazon pozíciójában
        #       - másik pozícióban
        #   - másik plugincontiner valamelyik pozíciójában
        #   - plugincontaineren kívül, üres területen
        #       - ha csak egy plugin van a forrás plugincontainer-ben, akkor ne történjen semmi (értelmetlen)

        # box_set_all()

        plugincontainer_target = None
        plugin_id_target = None

        for widget_id in self.canvas.plugincontainer_get().keys():
            widget_box = self.canvas.bbox(f"{widget_id}*background")
            x1, y1, x2, y2 = widget_box
            if canvas_x >= x1 and canvas_x <= x2 and canvas_y >= y1 and canvas_y <= y2:
                plugincontainer_target = widget_id
                for plugin_id, plugin_object in self.canvas.plugincontainer_get(plugincontainer_target).plugin_get().items():
                    plugin_object.box_set()
                    x1, y1, x2, y2 = plugin_object.box
                    if canvas_y >= y1 and canvas_y <= y2:
                        plugin_id_target = plugin_id

        if bool(plugincontainer_target):
            if plugincontainer_target == self.plugincontainer.id_get():
                # A plugin widgeten belül marad
                if bool(plugin_id_target):
                    if plugin_id_target == plugin_id_move:
                        # A widgeten belüli sorrend sem változik
                        print("Nothing changed")
                        # pass
                    else:
                        # A plugin pozíciója a widgeten belűl változik
                        print(f"There is'nt widget change, {plugin_id_move} plugin moves before {plugin_id_target} plugin")
                        self.plugincontainer.plugin_position_change(plugin_id_move, self.plugincontainer.plugin_position_get(plugin_id_target))
                else:
                    # A plugin a jelenlegi widget végére kerül
                    print(f"There is'nt widget change, {plugin_id_move} plugin moves the end of the widget")
            else:
                # widget váltás történik
                print(f"{plugin_id_move} plugin moves to {plugincontainer_target} widget ", end="")
                if bool(plugin_id_target):
                    # A plugin egy létező másik widgetben egy létező plugin elé kerül
                    print(f"before {plugin_id_target} plugin")
                    self.canvas.plugin_move(plugin_id_move, plugincontainer_id=plugincontainer_target)
                else:
                    # A plugin egy létező másik widget végére kerül
                    print("end")
                    self.canvas.plugin_move(plugin_id_move, plugincontainer_id=plugincontainer_target)
        else:
            # A plugin egy új üres widgetbe kerül, de csak akkor, ha eleve nem egyedül volt az eredeti widgetben
            if self.plugincontainer.plugin_count_get() > 1:
                self.canvas.plugin_move(plugin_id_move, x=canvas_x, y=canvas_y)


    def settings_init(self):
        self.config = ttk.Frame(self)
        self.btn_config = tk.Button(self.config, image=self.__image_setting, compound=tk.CENTER)
        self.btn_config.grid(row=0, column=0, sticky="nswe")
        self.btn_config.bind('<Button-1>', lambda event: self.settings_open(event))


    def settings_open(self, event):
        print("Settings panel start", type(self), self.model.id_get())


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
        self.__input_container.update({input_id: InputLabel(self, id=input_id, plugin_id=self.model.id_get(), plugincontainer_id=self.plugincontainer.id_get(), canvas_object=self.canvas)})
        self.__input_container[input_id].grid(row=self.__input_row_counter, column=self.__gridcoulmn_input)
        self.__input_row_counter += 1


    def input_object_get(self, input_id):
        return self.__input_container[input_id]


    def input_value_set(self, input):
        self.__input_container[input].value_set(text=self.model.input_value_get(input))


    def output_init(self, output_id):
        self.__output_container.update({output_id: OutputLabel(self, id=output_id, plugin_id=self.model.id_get(), plugincontainer_id=self.plugincontainer.id_get(), canvas_object=self.canvas)})
        self.__output_container[output_id].grid(row=self.__output_row_counter, column=self.__gridcolumn_output)
        self.__output_row_counter += 1


    def output_object_get(self, output_id):
        return self.__output_container[output_id]


    def output_value_set(self, output):
        text = self.model.output_value_get(output)
        self.__output_container[output].value_set(text=text)


    def input_container_get(self):
        return self.__input_container


    def output_container_get(self):
        return self.__output_container


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
