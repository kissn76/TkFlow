import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import pluginbase
import pluginframe
import maincanvas
import plugincontainer
import settingswindow



can_main = None

# widget settings
widget_width_min = 200
widget_height_min = 0
widget_resizer_width = 3
widget_padding = 6
# widget settings end

# images
MAX_SIZE = (12, 12)

image_move = Image.open("./resources/icon/move.png")
image_move.thumbnail((16, 16))

image_directory = Image.open("./resources/icon/directory.png")
image_directory.thumbnail(MAX_SIZE)

image_work = Image.open("./resources/icon/scrawdriver.png")
image_work.thumbnail(MAX_SIZE)
# images end


class Mainwindow(tk.Tk):
    def __init__(self):
        global can_main, image_move, image_directory, image_work
        super().__init__()
        self.title("TkFlow")
        self.geometry("1200x400")
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.attributes("-alpha", 0.6)
        self.style = ttk.Style(self)

        image_move = ImageTk.PhotoImage(image_move)
        image_directory = ImageTk.PhotoImage(image_directory)
        image_work = ImageTk.PhotoImage(image_work)

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

        self.sidebar = ttk.Frame(self)
        self.available_plugins = pluginframe.Pluginframe(self.sidebar)
        self.selected_theme = tk.StringVar()
        self.available_plugins.pack(fill=tk.BOTH, expand=True)

        self.statusbar = ttk.Label(self, text="Statusbar")

        self.frm_main.grid(row=0, column=0, sticky="n, s, w, e")
        self.sidebar.grid(row=0, column=1, sticky="n, s, w, e")
        self.statusbar.grid(row=1, column=0, columnspan=2, sticky="n, s, w, e")
        self.frm_main.rowconfigure(0, weight=1)
        self.frm_main.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.after(0, self.run)


    def settings(self):
        dlg = settingswindow.SettingsWindow(self)
        notebook = ttk.Notebook(dlg)
        notebook.pack(pady=10, expand=True)

        theme_changer = ttk.LabelFrame(notebook, text='Themes')
        theme_changer.pack()

        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(theme_changer, text=theme_name, value=theme_name, variable=self.selected_theme, command=self.change_theme)
            rb.pack(expand=True, fill='both')

        notebook.add(theme_changer, text="Themes")

        dlg.transient(self)   # dialog window is related to main
        dlg.wait_visibility() # can't grab until window appears, so we wait
        dlg.grab_set()        # ensure all input goes to our window
        dlg.wait_window()


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


    def change_theme(self):
        self.style.theme_use(self.selected_theme.get())


    def run(self):
        for plugin_object in pluginbase.get_all().values():
            plugin_object.run()

        self.after(100, self.run)


    def quit(self):
        super().quit()
