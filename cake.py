import logging
from waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()


def start():
    logging.info("the cake is baked!")
    epd.init()
    epd.Clear()


def update():
    logging.info("have some cake...")
    epd.display(epd.getbuffer(Himage))


def stop():
    logging.info("the cake is a lie!")
    epd7in5.epdconfig.module_exit()
