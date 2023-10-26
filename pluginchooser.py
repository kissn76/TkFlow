from tkinter import ttk
from PIL import ImageTk
import json
import style
import maincanvas



class Pluginchooser(ttk.Treeview):
    def __init__(self, master: ttk.Frame, canvas: maincanvas.Maincanvas, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = canvas
        self.image_directory = ImageTk.PhotoImage(style.image_directory_12)
        self.image_work = ImageTk.PhotoImage(style.image_work_12)
        self.floating_widget = None
        self.load()


    def load(self):
        self.plugin_categories = {}
        self.plugin_element_counter = 0

        pluginjson = None
        with open('plugins/plugins.json') as f:
            pluginjson = json.load(f)

        # add available plugin to gui
        def add(plugin):
            for plugin_parent_path in plugin["parents"]:
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
                self.insert(tree_master, 'end', f"plugin:{plugin['file'].split('.')[0]}.{self.plugin_element_counter}", text=plugin["name"], image=self.image_work)
                self.plugin_element_counter += 1
                self.bind('<<TreeviewSelect>>', lambda event: self.dnd_start(event, self.selection()))
                self.bind('<B1-Motion>', lambda event: self.dnd_motion(event))
                self.bind('<ButtonRelease-1>', lambda event: self.dnd_stop(event, self.selection()))

        for plugin in pluginjson:
            add(plugin)


    # plugin list methods
    def dnd_start(self, event, selection):
        entry_type, entry_name = selection[0].split(':')
        if entry_type == "plugin":
            plugin_id = entry_name.split('.')[0]

            self.floating_widget = ttk.Label(self.winfo_toplevel(), text=plugin_id)
            display_x, display_y, _, _ = self.canvas.cursor_position_get()
            self.floating_widget.place(x=display_x, y=display_y)


    def dnd_motion(self, event):
        if bool(self.floating_widget):
            display_x, display_y, _, _ = self.canvas.cursor_position_get()
            self.floating_widget.place(x=display_x, y=display_y)

            if not self.canvas.is_cursor_in_canvas():
                self.config(cursor="X_cursor")
            else:
                self.config(cursor="")


    def dnd_stop(self, event, selection):
        self.config(cursor="")

        if bool(self.floating_widget):
            self.floating_widget.place_forget()
            self.floating_widget.destroy()
            self.floating_widget = None

        entry_type, entry_name = selection[0].split(':')
        if entry_type == "plugin":
            plugin_name = entry_name.split('.')[0]

            if self.canvas.is_cursor_in_canvas():
                self.canvas.plugin_add(plugin_name)
