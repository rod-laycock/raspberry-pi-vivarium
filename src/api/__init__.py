# /api/__init__.py

#region Imports
import json
import threading
import time

from flask import Flask, request, Response, jsonify
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from json2html import *
from .models.sensor import Sensor, SensorEncoder, SensorReader
from python_json_config import ConfigBuilder
from typing import Dict
#endregion

#region Constants and Variables
API_DIRECTORY = ''
API_VERSION = '/v1'
API_ROOT = API_DIRECTORY + API_VERSION
SWAGGER_URL = API_ROOT + '/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = API_ROOT + '/swagger'  # Our API url (can of course be a local resource)

app = Flask(__name__)
app.debug = True

sensors: Dict[str, Sensor] = {}
pollFrequency: int = 0
mode: str = ""
temp_unit: str  = "C"
datetime_timezone: str = "UTC"
datetime_format: str = "%d/%m/%Y %H:%M:%S"
server_host: str = "127.0.0.1"
server_port: int = 5000
server_debug: bool = False
#endregion

#region Classes
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

            time.sleep(pollFrequency)
#endregion

#region Common routines to help with all the API requests

def get_format(request):
    format = request.mimetype
    if (format):
         format = str.lower(format)
         return format
    
    return "application/json"

def format_response(request, req_data):
    format = get_format(request)

    if (req_data is None):
        return Response("No data found", status=404, content_type=get_format(request))

    res_data = json.dumps(req_data, indent=2, separators=(',', ':'), cls=SensorEncoder, sort_keys=0)

    if (format is None):
        return "Unknown format requested", 400
    else:
        if (format == "text/html"):
            res_data = json2html.convert(json = res_data, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
        elif (format == "application/json"):
            pass
        else:
            return "Invalid format requested", 400

    return Response(res_data, status=200, content_type=get_format(request))

#endregion

#region Configuration
#
# Config - Get the current config values, factory default values and any allowable values.
#
def read_config(config: str):
    with open("/home/rod/Projects/Code/raspberry-pi-vivarium/src/webservice/config/" + config + ".json", "r") as config_file:
        return json.loads(config_file.read())
#endregion

#region routing
@app.route("/", methods=["GET"], )
def get_home():
    swagger_url = request.host_url + SWAGGER_URL
    return Response("Vivarium Monitoring Application up and running - please see <a href=\"" + swagger_url + "\">" + swagger_url + "</a> for how tro use the API.", status=200, mimetype="text/html")

@app.route(API_ROOT + "/swagger", methods=["GET"], )
def get_swagger_json():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Vivarium monitoring station"

    return jsonify(swag)

#
# Sensors - Get latest sensor data and configuration
#
@app.route(API_ROOT + "/sensors", methods=["GET"], )
def get_sensors():
    """
        List all sensors configuration and current data
        ---
        tags:
          - Sensors
        
        responses:
          200:
            description: Sensors data returned.
          400:
            description: Invalid data format requested.
          404:
            description: No sensors configured in the config/config.json file.
        """
    return format_response(request, sensors)

@app.route(API_ROOT + "/sensors/<int:port>", methods=["GET"])
def get_sensor_by_id(port: int):
    """
        Gets sensors configuration and current data of a specific sensor by port number
        ---
        tags:
          - Sensors
        
        responses:
          200:
            description: Sensor data returned.
          400:
            description: Invalid data format requested.
          404:
            description: No sensors configured in the config/config.json file.
    """
    return format_response(request, sensors.get(str(port)))

#
# Sensors - Get latest sensor data only
#
@app.route(API_ROOT + "/sensors/data", methods=["GET"], )
def get_sensors_data():
    """
        Gets just the sensor data for all sensors
        ---
        tags:
          - Sensors
        
        responses:
          200:
            description: Sensor data returned.
          400:
            description: Invalid data format requested.
          404:
            description: No sensors configured in the config/config.json file.
    """
    output_sensors = []
    for sensor in sensors:
        output_sensor = {}
        output_sensor["name"] = sensors[sensor].name
        output_sensor["temperature"] = sensors[sensor].temperature
        output_sensor["humidity"] = sensors[sensor].humidity
        output_sensors.append(output_sensor)
    return format_response(request, output_sensors)

    # return json2html.convert(json = , table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
    return "..."

@app.route(API_ROOT + "/sensors/data/<int:port>", methods=["GET"])
def get_sensor_data_by_id(port: int):
    """
        Gets just the sensor data for the sensor specified by the port
        ---
        tags:
          - Sensors
        
        responses:
          200:
            description: Sensor data returned.
          400:
            description: Invalid data format requested.
          404:
            description: No sensors configured in the config/config.json file.
    """    
    sensor = sensors.get(str(port))
    output_sensor = {}
    output_sensor["name"] = sensor.name
    output_sensor["temperature"] = sensor.temperature
    output_sensor["humidity"] = sensor.humidity
    
    return format_response(request, output_sensor)

#
# Configuration
#
@app.route(API_ROOT + "/config/current", methods=["GET"])
@app.route(API_ROOT + "/config", methods=["GET"])
def get_current_config():
    """
        Gets just the current configuration for the application
        ---
        tags:
          - Config
        
        responses:
          200:
            description: Config data returned.
          400:
            description: Invalid data format requested.
          404:
            description: Invalid config in the config/config.json file.
    """
    config = read_config("config")
    return format_response(request, config)


@app.route(API_ROOT + "/config/factory", methods=["GET"])
def get_factory_config():
    """
        Gets just the factory default configuration for the application
        ---
        tags:
          - Config
        
        responses:
          200:
            description: Config data returned.
          400:
            description: Invalid data format requested.
          404:
            description: Invalid config in the config/config.json file.
    """
    return read_config("factory")


@app.route(API_ROOT + "/config/values", methods=["GET"])
def get_config_values():
    """
        Gets default values which can be used when setting the config.json
        ---
        tags:
          - Config
        
        responses:
          200:
            description: Config defaults data returned.
          400:
            description: Invalid data format requested.
          404:
            description: Invalid config in the config/config.json file.
    """    
    return read_config("defaults")

#endregion



# Register the Swagger blueprint
# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Vivarium Monitoring Application"

    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)
app.register_blueprint(swaggerui_blueprint)

# Read the configuration file
# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config("/home/rod/Projects/Code/raspberry-pi-vivarium/src/api/config/config.json")

# access elements
server_host = config.Server.Host
server_port = config.Server.Port
server_debug = config.Server.Debug

for sensor in config.Sensors:
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

# with open("/home/rod/Projects/Code/raspberry-pi-vivarium/src/webservice/config/config.json", "r") as configFile:
#     configData = configFile.read()

# config = json.loads(configData)

# if config:
#     if "Server" in config:
#         if "Host" in config["Server"]:
#             server_host = config["Server"]["Host"]

#         if "Port" in config["Server"]:
#             server_port = config["Server"]["Port"]

#         if "Debug" in config["Server"]:
#             server_debug = bool(strtobool(config["Server"]["Debug"]))

#     poll_frequency = config["PollFrequency"]
#     mode = config["Mode"]
#     temp_unit = str(config["TempUnit"])
#     datetime = config["DateTime"]
#     datetime_timezone = datetime["TimeZone"]
#     datetime_format = datetime["Format"]

#     if "Sensors" in config:
#         for sensor in config["Sensors"]:
#             port = sensor["Port"]
#             sensorObj = Sensor(
#                 sensor["Name"],
#                 port,
#                 sensor["Pin"],
#                 sensor["SensorType"],
#                 sensor["Comment"],
#                 sensor["MinTemp"],
#                 sensor["MaxTemp"],
#                 sensor["MinHumidity"],
#                 sensor["MaxHumidity"],
#             )
#             sensors[str(port)] = sensorObj

sensorReaderWorkerThread = SensorReaderProcess()
sensorReaderWorkerThread.start()

#   worker = Worker(sensors, DateTime_Format, pollFrequency)
#   worker.start()
