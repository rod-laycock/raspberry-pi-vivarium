# Vivarium
#   Name - This will be the overall title / heading of the monitoring application.
#   Location - The location of this vivarium, so we can find it.
#   

class Vivarium():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.sensors = {}