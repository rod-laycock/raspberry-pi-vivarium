# from datetime import datetime
# from Models.Sensor import Sensor
# import json
# import time
# from Models.SensorReader import SensorReader

# sensors = {}


# # read file
# with open('Config/config.json', 'r') as configFile:
#     configData = configFile.read()

# # parse file
# config = json.loads(configData)


# # show values
# pollFrequency = config['PollFrequency']
# sensorCounter = 1
# mode = config['Mode']
# tempUnit = config['TempUnit']
# DateTime = config['DateTime']
# DateTime_TimeZone = DateTime['TimeZone']
# DateTime_Format = DateTime['Format']

# # Load the sensors read from config into the sensor dictionary
# for sensor in config['Sensors']:
#     port = sensor['Port']
#     s = Sensor(sensor['Name'], port, sensor['Pin'], sensor['SensorType'], sensor['Comment'], sensor['MinTemp'], sensor['MaxTemp'], tempUnit)
#     sensors[str(port)] = s

# sensorReader = SensorReader(mode)

# while True:
#     for sensorPort in sensors:
#         if sensorPort != None:
#             sensor = sensors[sensorPort]
#             dateTime, humidity, temperature = SensorReader.Read_Values(sensor)
#             localtime = time.strftime(DateTime_Format, dateTime)

#             if humidity is not None and temperature is not None:
#                 print("{1}: {0} Temp={2:0.1f}*C Hunmidity={3:0.1f}%".format(sensor.name, localtime, temperature, humidity))
#             else:
#                 print("Failed to retreive data from sensor")
#         time.sleep(pollFrequency)
