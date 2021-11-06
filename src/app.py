from Models.Sensor import Sensor
import json
import time

# from Models.SensorReader import SensorReader

sensors = {}


# read file
with open('Config/config.json', 'r') as configFile:
    configData = configFile.read()

# parse file
config = json.loads(configData)


# show values
pollFrequency = config['PollFrequency']
maxSensors = config['MaxSensors']
sensorCounter = 1

tempUnit = config['TempUnit']


for sensor in config['Sensors']:
    port = sensor['Port']
    s = Sensor(sensor['Name'], port, sensor['Pin'], sensor['Comment'], sensor['MinTemp'], sensor['MaxTemp'], tempUnit)
    sensors[str(port)] = s

# sensorReader = SensorReader(config['SensorType'])

# while True:
#     for sensor in sensors:
#         if sensor.
#     sSensorReader

# 	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
# 	localtime = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime())

# 	if humidity is not None and temperature is not None:
# 		print("{0}: Temp={1:0.1f}*C Hunmidity={2:0.1f}%".format(localtime, temperature, humidity))
# 	else:
# 		print("Failed to retreive data from sensor")
# 	time.sleep(pollFrequency)



print(sensors.values())    
#print("eur: " + str(obj['eur']))
#print("gbp: " + str(obj['gbp']))
#s1 = Sensor("Nagini - Hot", 1)





#print(s1.Get_Pin())
#print(s1.Get_Port())
#sensors[1] = Sensor("Nagini - Hot", 1)
#sensors[2] = Sensor("Nagini - Cold", 2)
#print(sensors)