# This is a stub so that it runs on my laptop
from datetime import datetime

class Adafruit_DHT():
  DHT11 = 1
  DHT22 = 2

  def read_retry(DHT_SENSOR, pin):
    now = datetime.now()
    
    humidity = now.min
    temperature = now.second
    
    return humidity, temperature