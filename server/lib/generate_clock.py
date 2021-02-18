import time
from PIL import Image, ImageDraw, ImageFont
import os
import io


# This is assuming the display is landscape, rather than vertical.
height = 122
width = 250

font18 = ImageFont.truetype('server/fonts/Font.ttc', 18)
font64 = ImageFont.truetype('server/fonts/Font.ttc', 64)


def run_command():
    time_image = Image.new('1', (width, height), 255)
    time_draw = ImageDraw.Draw(time_image)

    time_draw.rectangle((0, 0, 250, 122), fill=255)
    time_draw.text((0, 0), time.strftime('%H:%M'), font=font64, fill=0)
    time_draw.text((0, 100), time.strftime('%a, %d %B (%Y)'),
                   font=font18, fill=0)

    time_image = time_image.transpose(Image.ROTATE_180)
    img_byte_arr = io.BytesIO()
    time_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr
