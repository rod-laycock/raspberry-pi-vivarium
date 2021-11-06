#import Adafruit_DHT
import time

class SensorReader():
  DHT_SENSOR = Adafruit_DHT.DHT11
  MODE = None

  def __init__(self, mode):
    self.MODE = mode
  
  def Read_Values(self, sensor):
    # Production code
    if sensor.sensorType == "DHT11":
      DHT_SENSOR = Adafruit_DHT.DHT11
    elif sensor.sensorType == "DHT22":
      DHT_SENSOR = Adafruit_DHT.DHT22
    
    if MODE == "Dev":
      humidity = sensor.pin * 20
      temperature = sensor.port * 20
    else:
      humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.Get_Pin())

    return humidity, temperature

