import tkinter as tk
from tkinter import ttk
import plugincontroller
import pluginbase



__container = {}
__widget_plugin_connection = {}


def get(widget_id):
    object = None
    try:
        object = __container[widget_id]
    except:
        pass
    return object


def get_all():
    return __container


def widget_plugin_insert(widget_id, plugin_id):
    __widget_plugin_connection[widget_id].append(plugin_id)


def widget_plugins_get(widget_id):
    return __widget_plugin_connection[widget_id]


def widget_plugins_get_all():
    return __widget_plugin_connection


def widget_id_get(plugin_id):
    for widget_id, plugin_list in __widget_plugin_connection.items():
        if plugin_id in plugin_list:
            return widget_id

    return None



class Plugincontainer(ttk.Frame):
    def __init__(self, master, plugincontainer_id, **kwargs):
        super().__init__(master, **kwargs)
        self.id = plugincontainer_id
        add(self.id, self)
        self.__setting_mode = False


    def setting_mode_toggle(self):
        if self.__setting_mode:
            self.__setting_mode = False
        else:
            self.__setting_mode = True

        for plugin_object in self.plugins_get().values():
            plugin_object.setting_mode_set(self.__setting_mode)


    def setting_mode_get(self):
        return self.__setting_mode


    def plugin_insert(self, plugin_name):
        plugin_object = plugincontroller.new_object(plugin_name, self.id, master=self)
        plugin_object.pack(anchor="nw", fill=tk.BOTH)
        plugin_object.setting_mode_set(self.__setting_mode)
        pluginbase.add(plugin_object.id, plugin_object)
        widget_plugin_insert(self.id, plugin_object.id)


    def plugins_get(self):
        objects = {}
        plugins = widget_plugins_get(self.id)
        for plugin_id in plugins:
            objects.update({plugin_id: pluginbase.get(plugin_id)})

        return objects
