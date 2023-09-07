import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class WidgetBase(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.input_row_counter = 0
        self.output_row_counter = 0

        self.__input_container = {}
        self.__output_container = {}

        self.__input_area = ttk.Frame(self)
        self.__widget_area = ttk.Frame(self)
        self.__output_area = ttk.Frame(self)

        self.__input_area.grid(row=0, column=0, sticky="n, s, w, e")
        self.__widget_area.grid(row=0, column=1, sticky="n, s, w, e")
        self.__output_area.grid(row=0, column=2, sticky="n, s, w, e")

        self.columnconfigure(1, weight=1)


    def wiget_parent_get(self):
        return self.__widget_area


    def input_init(self, *args):
        for var_name in args:
            self.__input_container.update({var_name: InputLabel(self.__input_area)})
            self.__input_container[var_name].grid(row=self.input_row_counter, column=0, sticky="nse")
            self.input_row_counter += 1


    def input_value_set(self, input, value):
        try:
            self.__input_container[input].text_set(text=str(value))
        except:
            pass


    def input_value_get(self, input):
        return self.__input_container[input].text_get()


    def output_init(self, *args):
        for var_name in args:
            self.__output_container.update({var_name: OutputLabel(self.__output_area)})
            self.__output_container[var_name].grid(row=self.output_row_counter, column=0, sticky="nse")
            self.output_row_counter += 1


    def output_value_set(self, output, value):
        try:
            self.__output_container[output].text_set(text=str(value))
        except:
            pass



class InputLabel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        MAX_SIZE = (12, 12)
        datatype_any = Image.open(f"./resources/icon/anydata.png")
        data = Image.open(f"./resources/icon/arrow_right.png")
        datatype_any.thumbnail(MAX_SIZE)
        data.thumbnail(MAX_SIZE)
        self.image_anydata = ImageTk.PhotoImage(datatype_any)
        self.image_data = ImageTk.PhotoImage(data)

        self.lbl_txt = ttk.Label(self, text="a")
        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        self.lbl_data.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_txt.grid(row=0, column=2, sticky="n, s, w, e")


    def text_set(self, text):
        self.lbl_txt.configure(text=text)


    def text_get(self):
        return self.lbl_txt.cget("text")



class OutputLabel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        MAX_SIZE = (12, 12)
        datatype_any = Image.open(f"./resources/icon/anydata.png")
        data = Image.open(f"./resources/icon/arrow_right.png")
        datatype_any.thumbnail(MAX_SIZE)
        data.thumbnail(MAX_SIZE)
        self.image_anydata = ImageTk.PhotoImage(datatype_any)
        self.image_data = ImageTk.PhotoImage(data)

        self.lbl_txt = ttk.Label(self, text="a")
        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.grid(row=0, column=2, sticky="n, s, w, e")

        self.lbl_data.bind("<Button-1>", lambda event: self.dnd_start(event))
        self.lbl_data.bind('<B1-Motion>', lambda event: self.dnd_motion(event))


    def text_set(self, text):
        self.lbl_txt.configure(text=text)


    def text_get(self):
        return self.lbl_txt.cget("text")


    def dnd_start(self, event):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

        print((event.x, event.y), (self.winfo_pointerx(), self.winfo_pointery()), (self.winfo_rootx(), self.winfo_rooty()))


    def dnd_motion(self, event):
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()

        print((event.x, event.y), (self.winfo_pointerx(), self.winfo_pointery()), (self.winfo_rootx(), self.winfo_rooty()))
