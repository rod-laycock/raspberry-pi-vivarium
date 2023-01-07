import time
from json import JSONEncoder

from webservice.models.Adafruit_DHT import Adafruit_DHT

# Sensor
#   Name - so we can see it on screen
#   Port - Which port on the back of the system is this connected too?
#   Pin - So the sensor reader can request values on the pi
#   Comment - Human readable comment on this.
#   MinTemp - minimum temperature this sensor is allowed to get too
#   MaxTemp - maximum temperature this sensor is allowed to get too
#   Temp - this is the recorded temp
#   MinHumidity - minimum humidity this sensor is allowed to get too
#   MaxHumidity - maximum humidity this sensor is allowed to get too
#   Humidity - this is the recorded humidity

class Sensor():
    def __init__(self, name, port, pin, sensorType, comment, minTemp, maxTemp, minHumidity, maxHumidity):
        self.name = name
        self.port = port
        self.pin = pin
        self.sensorType = sensorType
        self.comment = comment
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.temp = 0
        self.minHumidity = minHumidity
        self.maxHumidity = maxHumidity
        self.humidity = 0

# Json Encoder 
class SensorEncoder(JSONEncoder):
    def default(self, s):
        return s.__dict__

# Mechanism to read data back from the sensors
class SensorReader():

  @staticmethod
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
    #   temperature = random(sensor.minTemp, sensor.maxTemp)
    # else:
    
    # humidity = 0
    # temperature = 0
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.pin)

    return time.localtime(), humidity, temperature
