from Models.BaseSensor import BaseSensor

# Sensor
#    Name - so we can see it on screen
#    Port - Which port on the back of the system is this connected too?

class Sensor():

    def __init__(self, name, port, pin, comment, minTemp, maxTemp, tempUnit):
        self.name = name
        self.port = port
        self.pin = pin
        self.comment = comment
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.tempUnit = tempUnit
    
  