import logging
from waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()


def start():
    logging.info("the dough is mixed!")
    epd.init()
    epd.Clear()


def update(Himage):
    logging.info("going in the oven...")
    epd.display(epd.getbuffer(Himage))
    logging.info("...done!")


def stop():
    logging.info("the cake is a lie!")
    epd7in5_V2.epdconfig.module_exit()
