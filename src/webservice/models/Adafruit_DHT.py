# This is a stub so that it runs on my laptop
from datetime import datetime
import random


class Adafruit_DHT:
    DHT11 = 1
    DHT22 = 2

    # this is a stub which can be used instead of the real Adafruit_DHT.read_retry method.
    #    This does not need to have a real sensor attached to it.
    @staticmethod
    def read_retry(DHT_SENSOR, pin):
        humidity = random.uniform(10.5, 75.5)
        temperature = random.uniform(10.5, 75.5)

        return humidity, temperature
