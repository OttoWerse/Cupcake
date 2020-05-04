import logging
from waveshare_epd import epd7in5_V2


def start():
    logging.info("epd7in5_V2 Demo")
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()


def update():
    epd.display(epd.getbuffer(Himage))


def stop():
    epd7in5.epdconfig.module_exit()



