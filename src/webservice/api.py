import json
import threading
import time

from distutils.util import strtobool
from flask import Flask
from flask_restful import Api
from models.sensor import Sensor, SensorEncoder, SensorReader

app = Flask(__name__)
api = Api(app)

sensors = {}
pollFrequency = 0
mode = ''
tempunit = "C"
datetime_timezone = "UTC"
datetime_format = "%d/%m/%Y %H:%M:%S"
server_host = "127.0.0.1"
server_port = 5000
server_debug = False

class SensorReaderProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            for sensorPort in sensors:
                if sensorPort != None:
                    sensor = sensors[sensorPort]
                    humidity = 0
                    temperature = 0

                    dateTime, humidity, temperature = SensorReader.Read_Values(sensor)
                    # localtime = time.strftime(datetime_format, time.localtime)

                    if humidity is not None and temperature is not None:
                        sensor.temperature = temperature
                        sensor.humidity = humidity
                    else:
                        sensor.temperature = 0
                        sensor.humidity = 0

            time.sleep(poll_frequency)

#
# Sensors - Get latest sensor data
#
@app.route('/sensors', methods=['GET'])
@app.route('/sensors/', methods=['GET'])
def get_sensors():
    return json.dumps(sensors, indent=2, cls=SensorEncoder)

# TODO: Return data 
@app.route('/sensors/<int:port>', methods=['GET'])
def get_sensor_by_id(port):
    sensor = sensors.get(str(port))
    return json.dumps(sensor, indent=2, cls=SensorEncoder)


#
# Config - Get the current config values, factory default values and any allowable values.
#
def read_config(config):
    with open('config/' + config + '.json', 'r') as configFile:
        configData = configFile.read()
    
    config = json.loads(configData)
    
    return config

@app.route('/config/current', methods=['GET'])
def get_current_config():
    return read_config('config')

@app.route('/config/factory', methods=['GET'])
def get_factory_config():
    return read_config('factory')

@app.route('/config/values', methods=['GET'])
def get_config_values():
    return read_config('defaults')

if __name__ == 'api':
    # Read the configuration file
    with open('config/config.json', 'r') as configFile:
        configData = configFile.read()
   
    config = json.loads(configData)

    if (config != None):
        if ('Server' in config):
            if ('Host' in config['Server']):
                server_host = config['Server']['Host']

            if ('Port' in config['Server']):
                server_port = config['Server']['Port']
            
            if ('Debug' in config['Server']):
                server_debug = bool(strtobool(config['Server']['Debug']))
        
        poll_frequency = config['PollFrequency']
        mode = config['Mode']
        temp_unit = str(config['TempUnit'])
        datetime = config['DateTime']
        datetime_timezone = datetime['TimeZone']
        datetime_format = datetime['Format']

        if ('Sensors' in config):
            for sensor in config['Sensors']:
                port = sensor['Port']
                sensorObj = Sensor(sensor['Name'], port, sensor['Pin'], sensor['SensorType'], sensor['Comment'], sensor['MinTemp'], sensor['MaxTemp'], sensor['MinHumidity'], sensor['MaxHumidity'])
                sensors[str(port)] = sensorObj
        
    sensorReaderWorkerThread = SensorReaderProcess()
    sensorReaderWorkerThread.start()

      #   worker = Worker(sensors, DateTime_Format, pollFrequency) 
      #   worker.start()

if __name__ == '__main__':
    app.run(debug=bool(server_debug), host = server_host, port = server_port)
