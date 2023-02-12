import time
from models.Adafruit_DHT import Adafruit_DHT

# lass to read data back from the sensor
class SensorReader():

    def __init__(self, sensor):
        self.sensor = sensor

    def Read_Values(sensor):
        if sensor.sensorType == "DHT11":
            DHT_SENSOR = Adafruit_DHT.DHT11
        elif sensor.sensorType == "DHT22":
            DHT_SENSOR = Adafruit_DHT.DHT22
        else:
            return time.localtime(), None, None

        # TODO: NEEDS TO BE REFACTORED - THIS SHOULD BE IN 1
        # if self.MODE == "Dev":
        #   humidity = random(sensor.minHumidity, sensor.maxHumidity)
        #   temperature = random(sensor.minTemperature, sensor.maxTemperature)
        # else:
        # humidity = 0
        # temperature = 0

        humidity, celcius = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.pin)

        if sensor.tempUnit[1].upper() == 'F':
            temperature = (celcius * 1.8) + 32   # Sensors return data in Celcius, convert it to Farenheit
        else:
            temperature = celcius
            
        return time.localtime(), humidity, temperature
