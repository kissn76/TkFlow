import tkinter as tk
from tkinter import ttk



class Plugincontainer(ttk.Frame):
    def __init__(self, master, plugincontainer_id, **kwargs):
        super().__init__(master, **kwargs)
        self.__id = plugincontainer_id
        self.__setting_mode = False
        self.__plugin_container = {}
        self.__plugin_order = []


    def id_get(self):
        return self.__id


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
        self.__plugin_order.append(id)
        self.__unpack_all()
        self.__pack_all()


    def __unpack_all(self):
        for plugin_object in self.plugin_get().values():
            plugin_object.pack_forget()


    def __pack_all(self):
        for plugin_id in self.__plugin_order:
            plugin_object = self.plugin_get(plugin_id)
            plugin_object.pack(anchor="nw", fill=tk.BOTH)


    def plugin_remove(self, plugin_id):
        plugin_view = self.__plugin_container.pop(plugin_id)
        plugin_view.pack_forget()
        plugin_view.destroy()


    def plugin_position_change(self, plugin_id, position_new):
        position_old = self.plugin_position_get(plugin_id)
        self.__plugin_order.pop(position_old)
        self.__plugin_order.insert(position_new, plugin_id)
        self.__unpack_all()
        self.__pack_all()


    def plugin_position_get(self, plugin_id):
        return self.__plugin_order.index(plugin_id)


    def plugin_get(self, plugin_id=None):
        plugin_object = None

        if bool(plugin_id):
            try:
                plugin_object = self.__plugin_container[plugin_id]
            except:
                pass
        else:
            plugin_object = self.__plugin_container

        return plugin_object


    def plugin_count_get(self):
        return len(self.__plugin_container)
