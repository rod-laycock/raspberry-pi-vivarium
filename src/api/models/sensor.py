
from json import JSONEncoder

from .Adafruit_DHT import Adafruit_DHT

# Sensor
#   Name - so we can see it on screen
#   Port - Which port on the back of the system is this connected too?
#   Pin - So the sensor reader can request values on the Rasperry Pi
#   Comment - Human readable comment on this.
#   minTemperature - minimum temperature this sensor is allowed to get too
#   maxTemperature - maximum temperature this sensor is allowed to get too
#   Temp - this is the recorded temp
#   MinHumidity - minimum humidity this sensor is allowed to get too
#   MaxHumidity - maximum humidity this sensor is allowed to get too
#   Humidity - this is the recorded humidity

class Sensor():
    def __init__(self, name, port, pin, sensorType, comment, minTemperature, maxTemperature, monitorTemperature, minHumidity, maxHumidity, monitorHumidity, temperatureUnit):
        self.name = name
        self.port = port
        self.pin = pin
        self.sensorType = sensorType
        self.comment = comment
        self.minTemperature = minTemperature
        self.maxTemperature = maxTemperature
        self.monitorTemperature = monitorTemperature
        self.currentTemperature = 0
        self.minHumidity = minHumidity
        self.maxHumidity = maxHumidity
        self.monitorHumidity = monitorHumidity
        self.currentHumidity = 0
        self.temperatureUnit = temperatureUnit

# Json Encoder 
class SensorEncoder(JSONEncoder):
    def default(self, s):
        return s.__dict__

