# Base Sensor - all the stuff which a Sensor can do is in here.

# Mapping from ports on back of device to pins on the IO board
# Subject to change should the 7" touch screen take over this.
PortPinMapping = {
    1: 29,  # GPIO 5 - pin 29
    2: 31,  # GPIO 6 - Pin 31
    3: 37,  # GPIO 26 - Pin 37
    4: 36,  # GPIO 16 - Pin 36 
    5: 22,  # GPIO 25 - Pin 22
    6: 16,  # GPIO 23 - Pin 16 
    7: 18,  # GPIO 24 - Pin 18
    8: 15   # GPIO 22 - Pin 15
    }

class BaseSensor():

    # Set the default temperature unit
    def __init__(self, tempUnit):
        self.tempUnit = tempUnit
        
    # Read the pin assigned to the port
    def Get_Pin(port):
        return PortPinMapping.get(port)

    # Read the port assigned to the pin
    def Get_Port(pin):
        for _port, _pin in PortPinMapping.items():
            if _pin == pin:
                return _port
        return None
        