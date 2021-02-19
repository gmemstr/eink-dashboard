#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from lib import epd2in13_V2
import time
import urllib2
from PIL import Image

from signal import signal, SIGINT
from sys import exit, argv

height = 122
width = 250


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


# Generate fallback image if unable to connect to server.
def generate_fallback():
    time_image = Image.new('1', (width, height), 255)
    time_draw = ImageDraw.Draw(time_image)

    time_draw.rectangle((0, 0, 250, 122), fill=255)
    time_draw.text((50, 50), time.strftime('%H:%M'), fill=0)
    time_draw.text((50, 100), time.strftime('%a, %d %B (%Y)'), fill=0)

    time_image = time_image.transpose(Image.ROTATE_180)

    return time_image


if __name__ == '__main__':
    signal(SIGINT, handler)

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Dashboard starting")

    epd = epd2in13_V2.EPD()
    logging.info("init and Clear")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    print("requesting from " + argv[1])
    try:
        try:
            i = Image.open(urllib2.urlopen(argv[1]))
        except Exception:
            i = generate_fallback()

        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(i))

        epd.init(epd.PART_UPDATE)
        last_updated = time.strftime("%M")
        while (True):
            if last_updated == time.strftime("%M"):
                time.sleep(1)
                continue

            try:
                i = Image.open(urllib2.urlopen(argv[1]))
            except Exception:
                i = generate_fallback()

            epd.displayPartial(epd.getbuffer(i))
            last_updated = time.strftime("%M")

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
