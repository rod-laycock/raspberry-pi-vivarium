from Models.Sensor import Sensor
import json

sensors = {}


# read file
with open('Config/config.json', 'r') as configFile:
    configData = configFile.read()

# parse file
config = json.loads(configData)


# show values
maxSensors = config['MaxSensors']
sensorCounter = 1

tempUnit = config['TempUnit']


for sensor in config['Sensors']:
    port = sensor['Port']
    s = Sensor(sensor['Name'], port, sensor['MinTemp'], sensor['MaxTemp'], tempUnit)
    sensors[str(port)] = s


print(sensors.values())    
#print("eur: " + str(obj['eur']))
#print("gbp: " + str(obj['gbp']))
#s1 = Sensor("Nagini - Hot", 1)





#print(s1.Get_Pin())
#print(s1.Get_Port())
#sensors[1] = Sensor("Nagini - Hot", 1)
#sensors[2] = Sensor("Nagini - Cold", 2)
#print(sensors)