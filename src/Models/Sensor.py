from Models.BaseSensor import BaseSensor

# Sensor
#    Name - so we can see it on screen
#    Port - Which port on the back of the system is this connected too?

class Sensor(BaseSensor):

    def __init__(self, name, pin, minTemp, maxTemp, tempUnit):
        self.name = name
        self.pin = pin
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        super().__init__(tempUnit)

    def Get_Pin(self):
        return BaseSensor.Get_Pin(self.pin)
    
    def GetPort(self):
        return BaseSensor.Get_Port(self.pin)
    
    
  