import tkinter as tk
from tkinter import ttk



class Pluginframe(ttk.Frame):
    def __init__(self, master, pluginframe_id, **kwargs):
        super().__init__(master, **kwargs)
        self.__id = pluginframe_id
        self.__setting_mode = False
        self.__pluginview_container = {}
        self.__pluginview_order = []


    def id_get(self):
        return self.__id


    def setting_mode_toggle(self):
        if self.__setting_mode:
            self.__setting_mode = False
        else:
            self.__setting_mode = True

        for pluginview_object in self.__pluginview_container.values():
            pluginview_object.setting_mode_set(self.__setting_mode)

        self.update()
        self.box_set()
        self.connect()


    def setting_mode_get(self):
        return self.__setting_mode


    def pluginview_insert(self, pluginview_object):
        self.__pluginview_container.update({pluginview_object.id_get(): pluginview_object})
        self.__pluginview_order.append(pluginview_object.id_get())
        pluginview_object.setting_mode_set(self.setting_mode_get())
        self.__unpack_all()
        self.__pack_all()


    def __unpack_all(self):
        for pluginview_object in self.pluginview_get().values():
            pluginview_object.pack_forget()


    def __pack_all(self):
        for plugin_id in self.__pluginview_order:
            pluginview_object = self.pluginview_get(plugin_id)
            pluginview_object.pack(anchor="nw", fill=tk.BOTH)


    def pluginview_remove(self, plugin_id):
        pluginview_object = self.__pluginview_container.pop(plugin_id)
        pluginview_object.pack_forget()
        pluginview_object.destroy()
        self.__pluginview_order.remove(plugin_id)


    def pluginview_position_change(self, plugin_id, position_new=None):
        position_old = self.pluginview_position_get(plugin_id)
        self.__pluginview_order.pop(position_old)

        if not position_new == None:
            self.__pluginview_order.insert(position_new, plugin_id)
        else:
            self.__pluginview_order.append(plugin_id)

        self.__unpack_all()
        self.__pack_all()


    def pluginview_position_get(self, plugin_id):
        ret = None
        if bool(plugin_id) and plugin_id in self.__pluginview_order:
            ret = self.__pluginview_order.index(plugin_id)

        return ret


    def pluginview_get(self, plugin_id=None):
        plugin_object = None

        if bool(plugin_id) and plugin_id in self.__pluginview_container.keys():
            plugin_object = self.__pluginview_container[plugin_id]
        else:
            plugin_object = self.__pluginview_container

        return plugin_object


    def pluginview_count_get(self):
        return len(self.__pluginview_container)


    def box_set(self):
        for plugin_view_object in self.pluginview_get().values():
            plugin_view_object.box_set()


    def connect(self):
        for plugin_view_object in self.pluginview_get().values():
            plugin_view_object.connect()
