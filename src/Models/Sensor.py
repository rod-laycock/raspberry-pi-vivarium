from Models.BaseSensor import BaseSensor

# Sensor
#    Name - so we can see it on screen
#    Port - Which port on the back of the system is this connected too?

class Sensor(BaseSensor):

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        super().__init__()

    def Get_Pin(self):
        return BaseSensor.Get_Pin(self.pin)
    
    def GetPort(self):
        return BaseSensor.Get_Port(self.pin)
    
    
  