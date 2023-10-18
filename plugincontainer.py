import tkinter as tk
from tkinter import ttk



class Plugincontainer(ttk.Frame):
    def __init__(self, master, plugincontainer_id, **kwargs):
        super().__init__(master, **kwargs)
        self.id = plugincontainer_id
        self.__setting_mode = False
        self.__plugin_container = {}


    def setting_mode_toggle(self):
        if self.__setting_mode:
            self.__setting_mode = False
        else:
            self.__setting_mode = True

        for plugin_object in self.__plugin_container.values():
            plugin_object.setting_mode_set(self.__setting_mode)


    def setting_mode_get(self):
        return self.__setting_mode


    def plugin_insert(self, id, plugin_object):
        self.__plugin_container.update({id: plugin_object})


    def plugins_get(self):
        return self.__plugin_container
