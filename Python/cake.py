import logging
from waveshare_epd import epd7in5_V2

epd = epd7in5_V2.EPD()


def start():
    logging.info("Init")
    epd.init()
    logging.info("Clear")
    epd.Clear()
    logging.info("Going to Sleep")
    epd.sleep()
    logging.info("Sleeping")


def update(Himage):
    logging.info("Init")
    epd.init()
    logging.info("Displaying")
    epd.display(epd.getbuffer(Himage))
    logging.info("Going to Sleep")
    epd.sleep()
    logging.info("Sleeping")


def stop():
    logging.info("Exiting")
    epd7in5_V2.epdconfig.module_exit()
    logging.info("Exited")
