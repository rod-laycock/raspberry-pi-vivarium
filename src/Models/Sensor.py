# Sensor
#   Name - so we can see it on screen
#   Port - Which port on the back of the system is this connected too?
#   Pin - So the sensor reader can request values on the pi
#   Comment - useless crap
#   MinTemp - minimum temperature this sensor is allowed to get too
#   MaxTemp - maximum temperature this sensor is allowed to get too 


class Sensor():

    def __init__(self, name, port, pin, sensorType, comment, minTemp, maxTemp, tempUnit):
        self.name = name
        self.port = port
        self.pin = pin
        self.sensorType = sensorType
        self.comment = comment
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.tempUnit = tempUnit
    
  