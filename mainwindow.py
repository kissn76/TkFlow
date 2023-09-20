import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import platform
import json
import pluginbase
import pluginframe
import maincanvas
import plugincontainer
import settingswindow
import style



can_main = None


class Mainwindow(tk.Tk):
    def __init__(self):
        global can_main
        super().__init__()
        self.title("TkFlow")

        self.geometry("1200x400")
        # self.attributes('-fullscreen', True)
        os_type = platform.system()
        if os_type == "Linux":
            self.attributes('-zoomed', True)
        else:   # Windows, Mac OS
            self.wm_state('zoomed')

        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.attributes("-alpha", 0.6)
        self.style = ttk.Style(self)

        self.image_move = ImageTk.PhotoImage(style.image_move)
        self.image_directory = ImageTk.PhotoImage(style.image_directory)
        self.image_work = ImageTk.PhotoImage(style.image_work)

        # Menubar
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New project", command=None)
        filemenu.add_command(label="Open project", command=None)
        filemenu.add_command(label="Save project", command=self.save)
        filemenu.add_command(label="Save project as...", command=None)
        filemenu.add_command(label="Close project", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Settings", command=self.settings)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # Canvas
        self.frm_main = ttk.Frame(self)
        can_main = maincanvas.Maincanvas(self.frm_main, scrollregion=(0, 0, 2000, 2000))
        hbar=ttk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL)
        hbar.grid(row=1, column=0, sticky="e, w")
        hbar.config(command=can_main.xview)
        vbar=ttk.Scrollbar(self.frm_main, orient=tk.VERTICAL)
        vbar.grid(row=0, column=1, sticky="n, s")
        vbar.config(command=can_main.yview)
        can_main.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        can_main.grid(row=0, column=0, sticky="n, s, w, e")
        can_main.rowconfigure(0, weight=1)
        can_main.columnconfigure(0, weight=1)
        can_main.bind('<Button-1>', can_main.dnd_start)
        can_main.bind('<Motion>', lambda event: self.statusbar.configure(text=f"{int(can_main.canvasx(event.x))}, {int(can_main.canvasy(event.y))}"))
        self.frm_main.grid(row=0, column=0, sticky="n, s, w, e")
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ttk.Frame(self)
        self.available_plugins = pluginframe.Pluginframe(self.sidebar)
        self.available_plugins.pack(fill=tk.BOTH, expand=True)
        self.sidebar.grid(row=0, column=1, sticky="n, s, w, e")

        # Statusbar
        self.statusbar = ttk.Label(self, text="Statusbar")
        self.statusbar.grid(row=1, column=0, columnspan=2, sticky="n, s, w, e")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.selected_theme = tk.StringVar()

        self.after(0, self.run)


    def settings(self):
        def set_settings():
            style.widget_width_min = var_width_min.get()
            style.widget_height_min = var_height_min.get()
            style.widget_resizer_width = var_resizer_width.get()
            style.widget_padding = var_padding.get()

            for plugincont in plugincontainer.get_all().values():
                can_main.widget_reset(plugincont.id)

            dlg.destroy()


        def change_color():
            colors = askcolor(title="Color Chooser")
            return colors[1]


        dlg = settingswindow.SettingsWindow(self)
        main = ttk.Frame(dlg)
        main.pack(expand=True, fill='both')
        notebook = ttk.Notebook(main)
        notebook.pack(expand=True, fill='both')
        buttons = ttk.Frame(main)
        buttons.pack(side=tk.BOTTOM)
        ttk.Button(buttons, text="Cancel", command=dlg.destroy).grid(row=0, column=0)
        ttk.Button(buttons, text="OK", command=set_settings).grid(row=0, column=1)

        appearance = ttk.Frame(notebook)
        appearance.pack(expand=True, fill='both')

        theme_changer = ttk.LabelFrame(appearance, text='Themes')
        theme_changer.pack(fill=tk.X)
        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(theme_changer, text=theme_name, value=theme_name, variable=self.selected_theme, command=self.change_theme)
            rb.pack(expand=True, fill='both')

        """
        widget_resizer_wh_color = "green"
        widget_background_color = "yellow"
        widget_background_outline_color = "blue"
        """

        widget_settings = ttk.LabelFrame(appearance, text='Widget Settings')
        widget_settings.pack(fill=tk.X)
        var_width_min = tk.IntVar(value=style.widget_width_min)
        var_height_min = tk.IntVar(value=style.widget_height_min)
        var_resizer_width = tk.IntVar(value=style.widget_resizer_width)
        widget_resizer_wh_width_multiplier = tk.IntVar(value=style.widget_resizer_wh_width_multiplier)
        var_padding = tk.IntVar(value=style.widget_padding)
        widget_width_resizer = tk.BooleanVar(value=style.widget_width_resizer)
        widget_height_resizer = tk.BooleanVar(value=style.widget_height_resizer)
        widget_width_height_resizer = tk.BooleanVar(value=style.widget_width_height_resizer)
        row = 0
        ttk.Label(widget_settings, text="Width min").grid(row=row, column=0)
        ttk.Entry(widget_settings, textvariable=var_width_min).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Height min").grid(row=row, column=0)
        ttk.Entry(widget_settings, textvariable=var_height_min).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Resizer width").grid(row=row, column=0)
        ttk.Entry(widget_settings, textvariable=var_resizer_width).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Width resizer enabled").grid(row=row, column=0)
        ttk.Checkbutton(widget_settings, variable=widget_width_resizer, onvalue=True, offvalue=False).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Height resizer enabled").grid(row=row, column=0)
        ttk.Checkbutton(widget_settings, variable=widget_height_resizer, onvalue=True, offvalue=False).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Width & height resizer enabled").grid(row=row, column=0)
        ttk.Checkbutton(widget_settings, variable=widget_width_height_resizer, onvalue=True, offvalue=False).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Width & height resizer width multiplier").grid(row=row, column=0)
        ttk.Entry(widget_settings, textvariable=widget_resizer_wh_width_multiplier).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Padding").grid(row=row, column=0)
        ttk.Entry(widget_settings, textvariable=var_padding).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Resizer color").grid(row=row, column=0)
        ttk.Button(widget_settings, text='Select a Color', command=change_color).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Width & height resizer color").grid(row=row, column=0)
        ttk.Button(widget_settings, text='Select a Color', command=change_color).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Widget background color").grid(row=row, column=0)
        ttk.Button(widget_settings, text='Select a Color', command=change_color).grid(row=row, column=1, sticky="w, e")
        row += 1
        ttk.Label(widget_settings, text="Widget background outline color").grid(row=row, column=0)
        ttk.Button(widget_settings, text='Select a Color', command=change_color).grid(row=row, column=1, sticky="w, e")
        row += 1
        widget_settings.columnconfigure(1, weight=1)

        notebook.add(appearance, text="Appearance")

        dlg.transient(self)   # dialog window is related to main
        dlg.wait_visibility() # can't grab until window appears, so we wait
        dlg.grab_set()        # ensure all input goes to our window
        dlg.wait_window()


    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())


    def save(self):
        project = self.to_dict()
        project_json = json.dumps(project, indent = 4)
        print(project_json)


    def to_dict(self):
        pcs_boxes = {}
        pcs_plugins = plugincontainer.widget_plugins_get_all()
        plugins = pluginbase.get_all_as_dict()
        for key in plugincontainer.get_all().keys():
            box = can_main.bbox(f"{key}:move")
            pcs_boxes.update({key: {"x": box[0], "y": box[1]}})

        project = {
            "plugins": plugins,
            "widget_plugins": pcs_plugins,
            "widget_positions": pcs_boxes
        }

        # print(plugins)
        # print(pcs_plugins)
        # print(pcs_boxes)

        return project


    def run(self):
        for plugin_object in pluginbase.get_all().values():
            plugin_object.run()

        self.after(100, self.run)


    def quit(self):
        super().quit()
