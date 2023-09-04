import tkinter as tk

root = tk.Tk()
root.state('normal')
widgets_to_zoom_list = []
DEFAULT_SIZE = 50


def zoom(widget):
    for every_widget in widgets_to_zoom_list:
        every_widget.config(width=widget.get(), height=widget.get())


def main():
    canvas = tk.Canvas(root)
    frame = tk.Frame(canvas)
    zoom_scale = tk.Scale(root, orient='vertical', from_=1, to=100)
    zoom_scale.config(command=lambda args: zoom(zoom_scale))

    zoom_scale.set(DEFAULT_SIZE)

    pixel = tk.PhotoImage(width=1, height=1)
    for i in range(50):
        btn = tk.Button(frame, text=str(i + 1), bg='Blue', image=pixel, width=DEFAULT_SIZE, height=DEFAULT_SIZE, compound="c")
        btn.grid(row=0, column=i)
        widgets_to_zoom_list.append(btn)

    canvas.create_window(0, 0, anchor='nw', window=frame)
    # make sure everything is displayed before configuring the scroll region
    canvas.update_idletasks()

    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.pack(fill='both', side='left', expand=True)
    zoom_scale.pack(fill='y', side='right')
    root.mainloop()


if __name__ == '__main__':
    main()