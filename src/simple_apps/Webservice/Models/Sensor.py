from json import JSONEncoder

# Sensor
#   Name - so we can see it on screen
#   Port - Which port on the back of the system is this connected too?
#   Pin - So the sensor reader can request values on the pi
#   Comment - Human readable comment on this.
#   MinTemp - minimum temperature this sensor is allowed to get too
#   MaxTemp - maximum temperature this sensor is allowed to get too
#   MinHumidity - minimum humidity this sensor is allowed to get too
#   MaxHumidity - maximum humidity this sensor is allowed to get too


class Sensor:
    def __init__(
        self,
        name,
        port,
        pin,
        sensorType,
        comment,
        minTemp,
        maxTemp,
        minHumidity,
        maxHumidity,
    ):
        self.name = name
        self.port = port
        self.pin = pin
        self.sensorType = sensorType
        self.comment = comment
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.minHumidity = minHumidity
        self.maxHumidity = maxHumidity


# Json Encoder
class SensorEncoder(JSONEncoder):
    def default(self, s):
        return s.__dict__
