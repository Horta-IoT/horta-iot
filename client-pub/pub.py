#!/usr/bin/env python

# Source: https://raw.githubusercontent.com/jpmens/tempgauge/master/boom.py

import paho
import paho.mqtt.client as mqtt
import random
import time
import sys

HOSTNAME = "mosquitto"
# HOSTNAME = "10.73.21.215"
PORT = 1883
TOPIC = "temp/random"

def log(topic, payload):
    sys.stderr.write("[pub][{}] > {:.1f}\n".format(topic, payload))
    sys.stderr.flush()

def error(message):
    sys.stderr.write("[pub][err] {}\n".format(message))
    sys.stderr.flush()

class sensor:
    def read():
        return random.uniform(10,40)

def main():
    mqttc = mqtt.Client()

    import logging
    logging.basicConfig(level=logging.DEBUG)
    mqttc.enable_logger()

    mqttc.connect(HOSTNAME, PORT)
    mqttc.loop_start()

    try:
        while True:
            payload = sensor.read()
            rc, mid = mqttc.publish(TOPIC, payload, qos=0, retain=False)
            if rc != 0:
                error("publish return value: {}".format(rc))
            else:
                log(TOPIC, payload)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        mqttc.loop_stop()
        mqttc.disconnect()

if __name__ == "__main__":
    main()
