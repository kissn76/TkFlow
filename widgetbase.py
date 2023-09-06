import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk



class WidgetBase(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

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
        row_counter = 0
        for var_name in args:
            self.__input_container.update({var_name: InputLabel(self.__input_area, text=var_name)})
            self.__input_container[var_name].grid(row=row_counter, column=0, sticky="nse")
            row_counter += 1


    def input_value_set(self, input, value):
        try:
            self.__input_container[input].configure(text=str(value))
        except:
            pass


    def input_value_get(self, input):
        return self.__input_container[input].cget("text")


    def output_init(self, *args):
        row_counter = 0
        for var_name in args:
            self.__output_container.update({var_name: OutputLabel(self.__output_area)})
            self.__output_container[var_name].grid(row=row_counter, column=0, sticky="nse")
            row_counter += 1


    def output_value_set(self, output, value):
        try:
            self.__output_container[output].text_set(text=str(value))
        except:
            pass



class InputLabel(ttk.Label):
    # def __init__(self, **kwargs):
    #     super(InputLabel, self).__init__(**kwargs)
    pass



class OutputLabel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        MAX_SIZE = (32, 32)
        ad = Image.open(f"./resources/icon/anydata.png")
        d = Image.open(f"./resources/icon/arrow_right.png")
        ad.thumbnail(MAX_SIZE)
        d.thumbnail(MAX_SIZE)
        self.image_anydata = ImageTk.PhotoImage(ad)
        self.image_data = ImageTk.PhotoImage(d)

        self.lbl_txt = ttk.Label(self, text="a")
        self.lbl_data_type = ttk.Label(self, image=self.image_anydata)
        self.lbl_data = ttk.Label(self, image=self.image_data)

        self.lbl_txt.grid(row=0, column=0, sticky="n, s, w, e")
        self.lbl_data_type.grid(row=0, column=1, sticky="n, s, w, e")
        self.lbl_data.grid(row=0, column=2, sticky="n, s, w, e")


    def text_set(self, text):
        self.lbl_txt.configure(text=text)


    def text_get(self):
        return self.lbl_txt.cget("text")
