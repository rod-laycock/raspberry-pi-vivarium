from Models.Sensor import Sensor

#import Adafruit_DHT
import time

class SensorReader():
  DHT_SENSOR = Adafruit_DHT.DHT22

  def __init__(self, dhtType):
    # if dhtType == 'DHT22':
    #   DHT_SENSOR = Adafruit_DHT.DHT22
    # elif dhtType == 'DHT11':
    #   DHT_SENSOR = Adafruit_DHT.DHT11
    # else:
      DHT_SENSOR = None
  
  def Read_Temp(self, sensor):
    # Production code
    #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensor.Get_Pin())
    
    # test code
    humidity = sensor.pin * 20
    temperature = sensor.port * 20

    return time.localtime(), humidity, temperature

