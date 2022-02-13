import json

import os
from flask import Flask
from flask_restful import Api
from distutils.util import strtobool
from Models.Sensor import Sensor, SensorEncoder
from worker import Worker

app = Flask(__name__)
api = Api(app)

# Variable to hold the sensors collection
sensors = {}


#
# Sensor
#
@app.route("/sensors", methods=["GET"])
def get_sensors():
    return json.dumps(sensors, indent=2, cls=SensorEncoder)


# TODO: Return data
@app.route("/sensors/<int:port>", methods=["GET"])
def get_sensor_by_id(port):
    sensor = sensors.get(str(port))
    return json.dumps(sensor, indent=2, cls=SensorEncoder)


#
# Config - Get the current config values, factory default values and any allowable values.
#
def read_config(config):
    with open("Config/" + config + ".json", "r") as configFile:
        configData = configFile.read()

    config = json.loads(configData)

    return config


@app.route("/config/current", methods=["GET"])
def get_current_config():
    return read_config("config")


@app.route("/config/factory", methods=["GET"])
def get_factory_config():
    return read_config("factory")


@app.route("/config/values", methods=["GET"])
def get_config_values():
    return read_config("defaults")


#
# Main entry point.
#
if __name__ == "__main__":
    # Defaults
    server_host = "127.0.0.1"
    server_port = 5000
    server_debug = False

    # Read the configuration file
    with open(os.getcwd() + "Config/config.json", "r") as configFile:
        configData = configFile.read()
    config = json.loads(configData)

    if config != None:
        if "Server" in config:
            if "Host" in config["Server"]:
                server_host = config["Server"]["Host"]

            if "Port" in config["Server"]:
                server_port = config["Server"]["Port"]

            if "Debug" in config["Server"]:
                server_debug = bool(strtobool(config["Server"]["Debug"]))

        pollFrequency = config["PollFrequency"]
        mode = config["Mode"]
        tempUnit = str(config["TempUnit"])
        DateTime = config["DateTime"]
        DateTime_TimeZone = DateTime["TimeZone"]
        DateTime_Format = DateTime["Format"]

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

        worker = Worker(sensors, DateTime_Format, pollFrequency)
        worker.start()
        app.run(debug=bool(server_debug), host=server_host, port=server_port)
