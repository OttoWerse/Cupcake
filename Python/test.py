# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5_V2
import time
from PIL import Image, ImageDraw, ImageFont

import paho.mqtt.client as mqtt
import traceback

logging.basicConfig(level=logging.DEBUG)


# Create function for receiving messages
def on_message(client, userdata, message):
    # decode message
    str = message.payload.decode("utf-8")

    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), str, font=font24, fill=0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(0)


# Create function for publishing callback
def on_publish(client, userdata, result):
    # print(result)
    pass


try:
    logging.info("epd7in5_V2 Demo")

    epd = epd7in5_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

    font24 = ImageFont.truetype(os.path.join(picdir, 'consola.ttf'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    # MQTT broker Settings
    broker = "192.169.4.5"
    port = 1883

    # Create MQTT client
    client = mqtt.Client("Cupcake2")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Start the loop
    # client.loop_start()

    client.subscribe('cupcake/mqtt-test/out')

    # Loop
    client.loop_forever()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5.epdconfig.module_exit()
    exit()
