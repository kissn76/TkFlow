from PIL import Image, ImageTk



# widget settings
widget_width_min = 200
widget_height_min = 0
widget_resizer_width = 6    # szám, páros szám
widget_width_resizer = True
widget_height_resizer = True
widget_resizer_wh_width_multiplier = 2
widget_resizer_color = "red"
widget_resizer_wh_color = "green"
widget_padding = 12
widget_background_color = "yellow"
widget_background_outline_color = "green"    # szín, 1 pixeles keret a background körül, "" kikapcsolja (üres string)
# widget settings end

# images
MAX_SIZE = (12, 12)

image_move = Image.open("./resources/icon/move.png")
image_move.thumbnail((16, 16))

image_directory = Image.open("./resources/icon/directory.png")
image_directory.thumbnail(MAX_SIZE)

image_work = Image.open("./resources/icon/scrawdriver.png")
image_work.thumbnail(MAX_SIZE)

datatype_any = Image.open(f"./resources/icon/anydata.png")
datatype_any.thumbnail(MAX_SIZE)

data = Image.open(f"./resources/icon/arrow_right.png")
data.thumbnail(MAX_SIZE)

image_setting = Image.open("./resources/icon/setting.png")
image_setting.thumbnail((16, 16))
# images end

widget_resizer_width = int(widget_resizer_width)
if widget_resizer_width %2 > 0:
    widget_resizer_width = int(widget_resizer_width + 1)