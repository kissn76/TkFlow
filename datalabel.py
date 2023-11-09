from tkinter import ttk
from PIL import ImageTk
import style



class DataLabel(ttk.Frame):
    def __init__(self, master, id, pluginview_object, pluginframe_object, canvas_object):
        super().__init__(master)
        self.__image_anydata = ImageTk.PhotoImage(style.image_datatype_any_12)
        self.__image_data = ImageTk.PhotoImage(style.image_data_12)

        self.__id = id
        self.__pluginview = pluginview_object
        self.__pluginframe = pluginframe_object
        self.__canvas = canvas_object

        self.__box = ()   # box in canvas

        self.__gui_style = ttk.Style()
        self.__gui_style.configure('My.TLabel', background='#334353')

        self._lbl_data = ttk.Label(self, image=self.__image_data)
        self._lbl_data.grid(row=0, column=0, sticky="n, s, w, e")
        self._lbl_data.bind("<Enter>", self.enter)
        self._lbl_data.bind("<Leave>", self.leave)


    def id_get(self):
        return self.__id


    def plugin_id_get(self):
        return self.__pluginview.id_get()


    def enter(self, event=None):
        self._lbl_data.configure(style="My.TLabel")


    def leave(self, event=None):
        self._lbl_data.configure(style="")


    def to_dict(self):
        ret = {self.__id: {"value": self.value_get()}}
        return ret


    def box_set(self, event=None):
        pluginframe_box = self.__canvas.bbox(f"{self.__pluginframe.id_get()}*pluginframe")
        plugin_geometry = self.master.winfo_geometry().replace('x', '+').split("+") # plugin geometry
        datalabel_geometry = self.winfo_geometry().replace('x', '+').split("+")     # [width, height, x, y] frame contains icons and value

        x1 = int(pluginframe_box[0]) + int(plugin_geometry[2]) + int(datalabel_geometry[2])
        y1 = int(pluginframe_box[1]) + int(plugin_geometry[3]) + int(datalabel_geometry[3])
        x2 = int(x1 + int(datalabel_geometry[0]))
        y2 = int(y1 + int(datalabel_geometry[1]))

        self.__box = (x1, y1, x2, y2)


    def box_get(self):
        return self.__box


    def pluginview_get(self):
        return self.__pluginview


    def canvas_get(self):
        return self.__canvas



class InputLabel(DataLabel):
    def __init__(self, master, id, pluginview_object, pluginframe_object, canvas_object):
        super().__init__(master, id, pluginview_object, pluginframe_object, canvas_object)
        self.__output_id = None
        self.__line_id = None
        self._lbl_data.bind('<Button-1>', self.__dnd_start)


    def __dnd_start(self, event):
        self._lbl_data.bind('<Button1-Motion>', self.__dnd_motion)
        self._lbl_data.bind('<ButtonRelease-1>', self.__dnd_stop)
        self.__output_id = self.pluginview_get().inputvariable_get(self.id_get())

        if bool(self.__output_id):
            self.__line_id = f"{self.__output_id}-{self.plugin_id_get()}:{self.id_get()}*connect_line"
        else:
            self.__line_id = "drawing"


    def __dnd_motion(self, event):
        if bool(self.__output_id):
            self.canvas_get().dnd_motion_datalabel(event, output_id=self.__output_id, line_tag=self.__line_id)
        else:
            self.canvas_get().dnd_motion_datalabel(event, input_id=f"{self.plugin_id_get()}:{self.id_get()}", line_tag=self.__line_id)


    def __dnd_stop(self, event):
        self._lbl_data.unbind('<Button1-Motion>')
        self._lbl_data.unbind('<ButtonRelease-1>')
        if bool(self.__output_id):
            self.pluginview_get().inputvariable_delete(self.id_get())
            self.canvas_get().dnd_stop_datalabel(event, output_id=self.__output_id, line_tag=self.__line_id)
        else:
            self.canvas_get().dnd_stop_datalabel(event, input_id=f"{self.plugin_id_get()}:{self.id_get()}", line_tag=self.__line_id)



class OutputLabel(DataLabel):
    def __init__(self, master, id, pluginview_object, pluginframe_object, canvas_object):
        super().__init__(master, id, pluginview_object, pluginframe_object, canvas_object)
        self.__output_id = f"{self.plugin_id_get()}:{self.id_get()}"
        self.__line_id = None
        self._lbl_data.bind('<Button-1>', self.__dnd_start)


    def __dnd_start(self, event):
        self.__line_id = "drawing"
        self._lbl_data.bind('<Button1-Motion>', self.__dnd_motion)
        self._lbl_data.bind('<ButtonRelease-1>', self.__dnd_stop)


    def __dnd_motion(self, event):
        self.canvas_get().dnd_motion_datalabel(event, output_id=self.__output_id, line_tag=self.__line_id)


    def __dnd_stop(self, event):
        self._lbl_data.unbind('<Button1-Motion>')
        self._lbl_data.unbind('<ButtonRelease-1>')
        self.canvas_get().dnd_stop_datalabel(event, output_id=self.__output_id, line_tag=self.__line_id)
