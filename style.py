from PIL import Image, ImageTk



# widget settings
widget_width_min = 200
widget_height_min = 0
widget_resizer_width = 2    # szám, páros szám
widget_width_resizer = True
widget_height_resizer = True
widget_width_height_resizer = False
widget_resizer_wh_width_multiplier = 2
widget_resizer_color = "red"
widget_resizer_wh_color = "green"
widget_padding = 6
widget_background_color = "yellow"
widget_background_outline_color = "blue"    # szín, 1 pixeles keret a background körül, "" kikapcsolja (üres string)
# widget settings end

# images
MAX_SIZE_6 = (6, 6)
MAX_SIZE_12 = (12, 12)
MAX_SIZE_16 = (16, 16)

image_move_16 = Image.open("./resources/icon/move.png")
image_move_16.thumbnail(MAX_SIZE_16)

image_arranger_12 = Image.open("./resources/icon/up-down.png")
image_arranger_12.thumbnail(MAX_SIZE_12)

image_up_6 = Image.open("./resources/icon/up.png")
image_up_6.thumbnail(MAX_SIZE_6)

image_down_6 = Image.open("./resources/icon/down.png")
image_down_6.thumbnail(MAX_SIZE_6)

image_directory_12 = Image.open("./resources/icon/directory.png")
image_directory_12.thumbnail(MAX_SIZE_12)

image_work_12 = Image.open("./resources/icon/scrawdriver.png")
image_work_12.thumbnail(MAX_SIZE_12)

image_datatype_any_12 = Image.open(f"./resources/icon/anydata.png")
image_datatype_any_12.thumbnail(MAX_SIZE_12)

image_data_12 = Image.open(f"./resources/icon/arrow_right.png")
image_data_12.thumbnail(MAX_SIZE_12)

image_setting_12 = Image.open("./resources/icon/setting.png")
image_setting_12.thumbnail(MAX_SIZE_12)

image_setting_16 = Image.open("./resources/icon/setting.png")
image_setting_16.thumbnail(MAX_SIZE_16)
# images end

widget_resizer_width = int(widget_resizer_width)
if widget_resizer_width %2 > 0:
    widget_resizer_width = int(widget_resizer_width + 1)