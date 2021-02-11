#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from lib import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont

from signal import signal, SIGINT
from sys import exit


def handler(signal_received, frame):
    # Handle any cleanup here
    logging.info('SIGINT or CTRL-C detected. Exiting gracefully')
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    logging.info("Goto Sleep...")
    epd.sleep()
    time.sleep(3)
    epd.Dev_exit()
    exit()


if __name__ == '__main__':
    signal(SIGINT, handler)

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Dashboard starting")

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    font18 = ImageFont.truetype('fonts/Font.ttc', 18)
    font64 = ImageFont.truetype('fonts/Font.ttc', 64)

    try:
        time_image = Image.new('1', (epd.height, epd.width), 255)
        time_draw = ImageDraw.Draw(time_image)

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(
            time_image.transpose(Image.ROTATE_180)))

        epd.init(epd.PART_UPDATE)
        last_time = ""
        while (True):
            if time.strftime('%H:%M') == last_time:
                time.sleep(5)
                continue

            time_draw.rectangle((0, 0, 250, 122), fill=255)
            time_draw.text((0, 0), time.strftime('%H:%M'), font=font64, fill=0)
            time_draw.text((0, 100), time.strftime('%a, %d %B (%Y)'),
                           font=font18, fill=0)

            epd.displayPartial(epd.getbuffer(time_image.transpose(
                Image.ROTATE_180)))
            last_time = time.strftime('%H:%M')
            time.sleep(1)
        # epd.Clear(0xFF)
        logging.info("Clear...")
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        logging.info("Goto Sleep...")
        epd.sleep()
        time.sleep(3)
        epd.Dev_exit()

    except IOError as e:
        logging.info(e)
