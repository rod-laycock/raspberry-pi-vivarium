import json
import threading
import time

from distutils.util import strtobool
from typing import Dict

from flask import Flask, request
from flask_restful import Api
from json2html import *
from models.sensor import Sensor, SensorEncoder, SensorReader
from models.sensor import Sensor


app = Flask(__name__)
api = Api(app)

sensors: Dict[str, Sensor] = {}
pollFrequency: int = 0
mode: str = ""
temp_unit: str  = "C"
datetime_timezone: str = "UTC"
datetime_format: str = "%d/%m/%Y %H:%M:%S"
server_host: str = "127.0.0.1"
server_port: int = 5000
server_debug: bool = False


class SensorReaderProcess(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            for sensorPort in sensors:
                if sensorPort:
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

def get_format(request):
    format = str.lower(request.args.get('format'))
    if (format):
        return format
    return "json"

def format_response(request, data):
    format = get_format(request)
    if (str.lower(format) == "html"):
        return json2html.convert(json = data, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")        
    return data

@app.route("/", methods=["GET"], )
def get_home():
    return "Python monitoring pythons is up and running."

#
# Sensors - Get latest sensor data and configuration
#
@app.route("/sensors", methods=["GET"], )
def get_sensors():
    data = json.dumps(sensors, indent=2, cls=SensorEncoder)
    return format_response(request, data)

@app.route("/sensors/<int:port>", methods=["GET"])
def get_sensor_by_id(port: int):
    data = json.dumps(sensors.get(str(port)), indent=2, cls=SensorEncoder)
    return format_response(request, data)


#
# Config - Get the current config values, factory default values and any allowable values.
#
def read_config(config: str):
    with open("/home/rod/Projects/Code/raspberry-pi-vivarium/src/webservice/config/" + config + ".json", "r") as config_file:
        return json.loads(config_file.read())

@app.route("/config/current", methods=["GET"])
@app.route("/config", methods=["GET"])
def get_current_config():
    return read_config("config")


@app.route("/config/factory", methods=["GET"])
def get_factory_config():
    return read_config("factory")


@app.route("/config/values", methods=["GET"])
def get_config_values():
    return read_config("defaults")


if __name__ == "__main__":

    # Read the configuration file
    with open("/home/rod/Projects/Code/raspberry-pi-vivarium/src/webservice/config/config.json", "r") as configFile:
        configData = configFile.read()

    config = json.loads(configData)

    if config:
        if "Server" in config:
            if "Host" in config["Server"]:
                server_host = config["Server"]["Host"]

            if "Port" in config["Server"]:
                server_port = config["Server"]["Port"]

            if "Debug" in config["Server"]:
                server_debug = bool(strtobool(config["Server"]["Debug"]))

        poll_frequency = config["PollFrequency"]
        mode = config["Mode"]
        temp_unit = str(config["TempUnit"])
        datetime = config["DateTime"]
        datetime_timezone = datetime["TimeZone"]
        datetime_format = datetime["Format"]

        if "Sensors" in config:
            for sensor in config["Sensors"]:
                port = sensor["Port"]
                sensorObj = Sensor(
                    sensor["Name"],
                    port,
                    sensor["Pin"],
                    sensor["SensorType"],
                    sensor["Comment"],
                    sensor["MinTemp"],
                    sensor["MaxTemp"],
                    sensor["MinHumidity"],
                    sensor["MaxHumidity"],
                )
                sensors[str(port)] = sensorObj

    sensorReaderWorkerThread = SensorReaderProcess()
    sensorReaderWorkerThread.start()

    #   worker = Worker(sensors, DateTime_Format, pollFrequency)
    #   worker.start()

    app.run(debug=bool(server_debug), host=server_host, port=server_port)
