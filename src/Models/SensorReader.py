from Models.Adafruit_DHT import Adafruit_DHT

class SensorReader():
  DHT_SENSOR = Adafruit_DHT.DHT11
  MODE = ""

  def __init__(self, mode):
    self.MODE = mode
  
  def Read_Values(self, sensor):
    # Production code
    if sensor.sensorType == "DHT11":
      self.DHT_SENSOR = Adafruit_DHT.DHT11
    elif sensor.sensorType == "DHT22":
      self.DHT_SENSOR = Adafruit_DHT.DHT22
    
    if self.MODE == "Dev":
      humidity = sensor.pin * 20
      temperature = sensor.port * 20
    else:
      humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, sensor.pin)

    return humidity, temperature

