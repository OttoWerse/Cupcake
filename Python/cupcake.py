# !/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import threading

curdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
assdir = os.path.join(curdir, "Assets")
libdir = os.path.join(curdir, 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from PIL import Image, ImageDraw, ImageFont
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)

debug = True

if debug:
    import cup
else:
    import cake

person = 'otto-werse'
room = 'ottos-room'

# margin_top = 10
# margin_bottom = 10
# margin_left = 10
# margin_right = 10

font_size = 32
spacing = 4

width = 800
height = 480

icon_size = 128

rows = 2
columns = 3
block_height = -(-height // rows)
block_width = -(-width // columns)

topics = {
    f'presence/residents/{person}/present/out': {
        'position': {
            'horizontal': 0,
            'vertical': 0, },
        'txt': None,
        'img': None,
        'true': {
            'txt': 'Zuhause',
            'img': 'home.png'},
        'false': {
            'txt': 'Abwesend',
            'img': 'home-off.png'},
    },
    f'presence/residents/{person}/sleeping/out': {
        'position': {
            'horizontal': 1,
            'vertical': 0, },
        'txt': None,
        'img': None,
        'true': {
            'txt': 'Schläft',
            'img': 'sleep.png'},
        'false': {
            'txt': 'Wach',
            'img': 'sleep-off.png'},
    },
    f'presence/residents/{person}/inbed/out': {
        'position': {
            'horizontal': 2,
            'vertical': 0, },
        'txt': None,
        'img': None,
        'true': {
            'txt': 'Im Bett',
            'img': 'bed.png'},
        'false': {
            'txt': 'Aufgestanden',
            'img': 'bed-off.png'},
    },
    f'presence/residents/{person}/donotdisturb/out': {
        'position': {
            'horizontal': 0,
            'vertical': 1, },
        'txt': None,
        'img': None,
        'true': {
            'txt': 'Nicht Stören!',
            'img': 'do-not-disturb.png'},
        'false': {
            'txt': 'Bitte Klopfen!',
            'img': 'check-circle.png'},
    },
    f'heating/{room}/window-state/out': {
        'position': {
            'horizontal': 1,
            'vertical': 1, },
        'txt': None,
        'img': None,
        '0': {
            'txt': 'Verschlossen',
            'img': 'window-off.png'},
        '1': {
            'txt': 'Offen',
            'img': 'window.png'},
        '2': {
            'txt': 'Offen',
            'img': 'window.png'},
    },
}


# Create function for receiving messages
def on_message(client, userdata, message):
    logging.info(f'MQTT Received on {message.topic}: {message.payload}')

    # Import Global
    global topics

    # decode message
    str = message.payload.decode("utf-8")

    # Process Message
    current = topics[message.topic]
    current['txt'] = current[str]['txt']
    current['img'] = current[str]['img']
    # print(current)

    logging.info('Checking for Topics...')

    missing = False

    for x in topics:
        if topics[x]['txt'] == None:
            missing = True
            logging.debug(f'Missing : {x}')

    if (missing):
        logging.info('Waiting for Topics')
    else:
        logging.info('Refreshing...')
        Himage = Image.new('1',
                           (
                               width,
                               height
                           ),
                           255)
        for x in topics:
            background = Image.new('1',
                                   (
                                       block_width,
                                       block_height
                                   ),
                                   0)
            box = Image.new('1',
                            (
                                block_width - 2,
                                block_height - 2
                            ),
                            255)

            try:
                # icon = Image.open('Pressed.png')
                path = os.path.join(assdir, topics[x]['img'])
                icon = Image.open(path)
                box.paste(icon,
                          (
                              (block_width - icon_size) // 2,
                              block_height - 2 * (font_size + spacing) - icon_size
                          ),
                          mask=icon)
            except:
                logging.error('Image not found!')

            draw = ImageDraw.Draw(box)
            content = topics[x]['txt']
            text_width, text_height = draw.textsize(content, font=consolas)
            draw.text(
                (
                    (block_width - text_width) / 2,
                    block_height - 2 * (font_size + spacing)
                ),
                content,
                font=consolas,
                fill=0
            )

            background.paste(box,
                             (
                                 0,
                                 0,
                             ))
            Himage.paste(background,
                         (
                             (topics[x]['position']['horizontal'] * block_width),
                             (topics[x]['position']['vertical'] * block_height),
                         ))
        # Process Image according to debug setting
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

    logging.debug("Loading Fonts")
    consolas = ImageFont.truetype(os.path.join(assdir, 'consola.ttf'), font_size)
    logging.debug("Done!")

    # MQTT broker Settings
    logging.debug("Starting MQTT")
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
    logging.debug("Done!")

    # Subscribe to Topics
    logging.debug("Subscribing Topics")
    for x in topics:
        logging.info(f'subscribing to {x}')
        client.subscribe(x)
    logging.debug("Done!")

    # Loop
    client.loop_forever()

except IOError as e:
    logging.error(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    if debug:
        cup.stop()
    else:
        cake.stop()
    exit()
