#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
from lib import epd2in13_V2
import time
import urllib2
from PIL import Image

from signal import signal, SIGINT
from sys import exit, argv


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
    print("requesting from " + argv[1])
    try:
        i = Image.open(urllib2.urlopen(argv[1]))
        epd.init(epd.FULL_UPDATE)
        epd.displayPartBaseImage(epd.getbuffer(i))

        epd.init(epd.PART_UPDATE)
        last_updated = time.strftime("%M")
        while (True):
            if last_updated == time.strftime("%M"):
                time.sleep(1)
                continue

            i = Image.open(urllib2.urlopen(argv[1]))

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
