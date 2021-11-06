from Models.Sensor import Sensor
import json
import time

from Models.SensorReader import SensorReader

sensors = {}


# read file
with open('Config/config.json', 'r') as configFile:
    configData = configFile.read()

# parse file
config = json.loads(configData)


# show values
pollFrequency = config['PollFrequency']
sensorCounter = 1
mode = config['Mode']
tempUnit = config['TempUnit']

# Load the sensors read from config into the sensor dictionary
for sensor in config['Sensors']:
    port = sensor['Port']
    s = Sensor(sensor['Name'], port, sensor['Pin'], sensor['SensorType'], sensor['Comment'], sensor['MinTemp'], sensor['MaxTemp'], tempUnit)
    sensors[str(port)] = s

sensorReader = SensorReader(mode)

while True:
    for sensorPort in sensors:
        if sensorPort != None:
            sensor = sensors[sensorPort]
            humidity, temperature = sensorReader.Read_Values(sensor)
            localtime = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime())

            if humidity is not None and temperature is not None:
                print("{1}: {0} Temp={2:0.1f}*C Hunmidity={3:0.1f}%".format(sensor.name, localtime, temperature, humidity))
            else:
                print("Failed to retreive data from sensor")
    time.sleep(pollFrequency)
    print("-----------------------------")



# for s in sensors:
#     x = sensors[s]   
#     print(x.name + '|' + str(x.pin) + '|' + str(x.port) + '|' + x.comment )    
#print("eur: " + str(obj['eur']))
#print("gbp: " + str(obj['gbp']))
#s1 = Sensor("Nagini - Hot", 1)





#print(s1.Get_Pin())
#print(s1.Get_Port())
#sensors[1] = Sensor("Nagini - Hot", 1)
#sensors[2] = Sensor("Nagini - Cold", 2)
#print(sensors)