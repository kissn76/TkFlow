import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import plugincontroller
import mainwindow
import style



class Pluginframe(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.image_directory = ImageTk.PhotoImage(style.image_directory_12)
        self.image_work = ImageTk.PhotoImage(style.image_work_12)
        self.floating_widget = None
        self.load()


    def load(self):
        self.plugin_categories = {}
        self.plugin_element_counter = 0

        # add available plugin to gui
        def add(plugin_name):
            plugin_object = plugincontroller.new_object(plugin_name, None, None, None)
            for plugin_parent_path in plugin_object.parents:
                parent_path = ""
                for parent_element in plugin_parent_path.split('/'):
                    parent_path_new = parent_path
                    if not parent_path_new == "":
                        parent_path_new += "/"
                    parent_path_new += parent_element

                    if not parent_path_new in self.plugin_categories.keys():
                        self.plugin_categories.update({parent_path_new: f"category:{self.plugin_element_counter}"})
                        tree_master = ""
                        tree_open = True
                        try:
                            tree_master = self.plugin_categories[parent_path]
                            tree_open = False
                        except:
                            pass
                        self.insert(tree_master, 'end', self.plugin_categories[parent_path_new], text=parent_path_new.split('/')[-1], image=self.image_directory, open=tree_open)
                        self.plugin_element_counter += 1

                    parent_path = parent_path_new

                tree_master = ""
                try:
                    tree_master = self.plugin_categories[parent_path]
                except:
                    pass
                self.insert(tree_master, 'end', f"plugin:{plugin_name}.{self.plugin_element_counter}", text=plugin_object.name, image=self.image_work)
                self.plugin_element_counter += 1
                self.bind('<<TreeviewSelect>>', lambda event: self.dnd_start(event, self.selection()))
                self.bind('<B1-Motion>', lambda event: self.dnd_motion(event))
                self.bind('<ButtonRelease-1>', lambda event: self.dnd_stop(event, self.selection()))

        for plugin_name in plugincontroller.list_plugins():
            add(plugin_name)


    # plugin list methods
    def dnd_start(self, event, selection):
        x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
        y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()

        entry_type, entry_name = selection[0].split(':')
        if entry_type == "plugin":
            plugin_id = entry_name.split('.')[0]

            self.floating_widget = ttk.Label(self.winfo_toplevel(), text=plugin_id)
            self.floating_widget.place(x=x, y=y)


    def dnd_motion(self, event):
        if bool(self.floating_widget):
            x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
            y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
            canvas_x = mainwindow.can_main.canvasx(x)
            canvas_y = mainwindow.can_main.canvasy(y)

            self.floating_widget.place(x=x, y=y)

            can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, mainwindow.can_main.cget("scrollregion").split()))

            if canvas_x <= 0 or canvas_y <= 0 or canvas_x >= can_main_width - style.widget_padding * 2 or canvas_y >= can_main_height - style.widget_padding * 2:
                self.config(cursor="X_cursor")
            else:
                self.config(cursor="")


    def dnd_stop(self, event, selection):
        self.config(cursor="")

        entry_type, entry_name = selection[0].split(':')
        if entry_type == "plugin":
            plugin_id = entry_name.split('.')[0]

            if bool(self.floating_widget):
                self.floating_widget.place_forget()
                self.floating_widget.destroy()
                self.floating_widget = None

            if event.x < 0:
                x = self.winfo_pointerx() - mainwindow.can_main.winfo_rootx()
                y = self.winfo_pointery() - mainwindow.can_main.winfo_rooty()
                canvas_x = mainwindow.can_main.canvasx(x)
                canvas_y = mainwindow.can_main.canvasy(y)

                can_main_x, can_main_y, can_main_width, can_main_height = list(map(int, mainwindow.can_main.cget("scrollregion").split()))
                if canvas_x > 0 and canvas_y > 0 and canvas_x < can_main_width - style.widget_padding * 2 and canvas_y < can_main_height - style.widget_padding * 2:
                    try:
                        widgets = mainwindow.can_main.find_overlapping(canvas_x - 1, canvas_y - 1, canvas_x + 1, canvas_y + 1)

                        if len(widgets) == 0:
                            mainwindow.can_main.widget_create(plugin_name=plugin_id, x=canvas_x, y=canvas_y)
                        else:
                            widget_ids = set()
                            for id in widgets:
                                tags = mainwindow.can_main.gettags(id)
                                if len(tags) > 0:
                                    widget_id, _ = tags[0].split('*')
                                    widget_ids.add(widget_id)

                            if len(widget_ids) == 1:
                                target_widget_id = list(widget_ids)[0]
                                plugincontainer = mainwindow.can_main.plugincontainer_get(target_widget_id)
                                mainwindow.can_main.plugin_add(plugin_id, plugincontainer)
                                self.winfo_toplevel().update()
                                mainwindow.can_main.widget_background_set(widget_id, keep_height=True)
                                mainwindow.can_main.widget_resizer_set(widget_id)

                                for plugin_object in plugincontainer.plugins_get().values():
                                    plugin_object.datalabels_box_set()
                                    plugin_object.connect(mainwindow.can_main.plugin_get_all())
                            else:
                                print("too many widget are overlapped:", widget_ids)
                    except:
                        pass
