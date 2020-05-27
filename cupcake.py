# !/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import threading

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from PIL import Image, ImageDraw, ImageFont
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.DEBUG)

debug = True

if debug:
    import cup
else:
    import cake

txt1 = None
txt2 = None
txt3 = None
txt4 = None

img1 = None
img2 = None
img3 = None
img4 = None

margin_top = 10
margin_bottom = 10
margin_left = 10
margin_right = 10

font_size = 64
spacing = 4

width = 800
height = 480


# Create function for receiving messages
def on_message(client, userdata, message):
    logging.info('MQTT Received')

    # Import Global
    global txt1, txt2, txt3, txt4

    # decode message
    str = message.payload.decode("utf-8")

    # Process Message
    if message.topic == 'presence/residents/otto-werse/present/out':
        logging.info(f'Present: {str}')
        if str == 'true':
            txt1 = 'Zuhause'
        elif str == 'false':
            txt1 = 'Abwesend'
    elif message.topic == 'presence/residents/otto-werse/asleep/out':
        logging.info(f'Sleep: {str}')
        if str == 'true':
            txt2 = 'Schlafend'
        elif str == 'false':
            txt2 = 'Wach'
    elif message.topic == 'presence/residents/otto-werse/in-bed/out':
        logging.info(f'Bed: {str}')
        if str == 'true':
            txt3 = 'Im Bett'
        elif str == 'false':
            txt3 = 'Aufgestanden'
    elif message.topic == 'heating/ottos-room/window-state/out':
        logging.info(f'Window: {str}')
        if str == '0':
            txt4 = 'Verschlossen'
        elif str == '1':
            txt4 = 'Angekippt'
        elif str == '2':
            txt4 = 'Offen'

    logging.info('Checking for Topics...')
    if txt1 is None:
        logging.info('Still waiting for MQTT (txt1)')
    elif txt2 is None:
        logging.info('Still waiting for MQTT (txt2)')
    elif txt3 is None:
        logging.info('Still waiting for MQTT (txt3)')
    elif txt4 is None:
        logging.info('Still waiting for MQTT (txt4)')
    else:
        # Drawing on the Horizontal image
        logging.info('Refreshing...')
        Himage = Image.new('1', (width, height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((margin_left + 0, (margin_top + 0 * (font_size + spacing))), txt1, font=consolas, fill=0)
        draw.text((margin_left + 0, (margin_top + 1 * (font_size + spacing))), txt2, font=consolas, fill=0)
        draw.text((margin_left + 0, (margin_top + 2 * (font_size + spacing))), txt3, font=consolas, fill=0)
        draw.text((margin_left + 0, (margin_top + 3 * (font_size + spacing))), txt4, font=consolas, fill=0)

        if debug:
            Himage.save('output.png')
            cup.update()
        else:
            cake.update(Himage)

        logging.info('Done!')


# Create function for publishing callback
def on_publish(client, userdata, result):
    # print(result)
    pass


try:
    logging.info("init and Clear")

    if debug:
        th = threading.Thread(target=cup.start)
        th.start()
    else:
        cake.start()

    consolas = ImageFont.truetype(os.path.join(picdir, 'consola.ttf'), font_size)

    # MQTT broker Settings
    broker = "192.169.0.203"
    port = 1883

    # Create MQTT client
    if debug:
        client = mqtt.Client("Cupcake-Debug")
    else:
        client = mqtt.Client("Cupcake")

    # Assign on methods
    client.on_publish = on_publish
    client.on_message = on_message

    # Connect to broker
    client.connect(broker, port)

    # Subscribe to Topics
    client.subscribe('presence/residents/otto-werse/present/out')
    client.subscribe('presence/residents/otto-werse/asleep/out')
    client.subscribe('presence/residents/otto-werse/in-bed/out')
    client.subscribe('heating/ottos-room/window-state/out')

    # Loop
    client.loop_forever()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    if debug:
        cup.stop()
    else:
        cake.stop()
    exit()
