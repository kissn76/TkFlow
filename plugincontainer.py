import tkinter as tk
from tkinter import ttk
import plugincontroller
import pluginbase



__container = {}
__counter = 0


def get(widget_id):
    object = None
    try:
        object = __container[widget_id]
    except:
        pass
    return object


def get_all():
    return __container


def add(widget_id, object):
    __container.update({widget_id: object})


def counter_get():
    global __counter
    ret = __counter
    __counter += 1
    return ret



class Plugincontainer(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.id = f"widget.{counter_get()}"
        add(self.id, self)


    def plugin_insert(self, plugin_name):
        plugin_object = plugincontroller.new_object(plugin_name, self.id, master=self)
        plugin_object.pack(anchor="nw", fill=tk.BOTH)
        pluginbase.add(plugin_object.id, plugin_object)


    def plugins_get(self):
        objects = {}
        for key, object in pluginbase.get_all().items():
            if key.startswith(self.id):
                objects.update({key: object})

        return objects
