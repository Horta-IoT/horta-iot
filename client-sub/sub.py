#!/usr/bin/env python

# Source: https://pypi.python.org/pypi/paho-mqtt/1.3.0

import paho.mqtt.client as mqtt
import sys

HOSTNAME = "mosquitto"
# HOSTNAME = "10.73.21.215"
PORT = 1883
TOPIC = 'temp/random'

def log(topic, payload):
    sys.stderr.write("[sub][{}] < {:.1f}\n".format(topic, payload))
    sys.stderr.flush()

def info(message):
    sys.stderr.write("[sub][info] {}\n".format(message))
    sys.stderr.flush()

def error(message):
    sys.stderr.write("[sub][err] {}\n".format(message))
    sys.stderr.flush()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc != 0:
        error("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    log(msg.topic, float(msg.payload))

def main():
    client = mqtt.Client()

    import logging
    logging.basicConfig(level=logging.DEBUG)
    client.enable_logger()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(HOSTNAME, PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        pass
        

if __name__ == "__main__":
    main()
