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
from models.sensor import Sensor, SensorEncoder
from models.server import Server
from models.vivaria import Vivaria
from models.vivarium import Vivarium
from models.sensorReader import SensorReader
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

vivaria: Vivaria


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
        for viv in vivaria.vivarium:
          for sensorPort in viv['sensors']:
            if sensorPort:
                sensor = viv['sensors'][sensorPort]
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
    with open("/home/rod/Projects/Code/raspberry-pi-vivarium/src/api/config/" + config + ".json", "r") as config_file:
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
    response = {}
    output_sensors = []
    for sensor in sensors:
        output_sensor = {}
        output_sensor["name"] = sensors[sensor].name
        output_sensor["minTemp"] = sensors[sensor].minTemp
        output_sensor["maxTemp"] = sensors[sensor].maxTemp
        output_sensor["temperature"] = sensors[sensor].temperature
        output_sensor["minHumidity"] = sensors[sensor].minHumidity
        output_sensor["maxHumidity"] = sensors[sensor].maxHumidity
        output_sensor["humidity"] = sensors[sensor].humidity
        output_sensor["tempUnit"] = sensors[sensor].tempUnit
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
    output_sensor["minTemp"] = sensor.minTemp
    output_sensor["maxTemp"] = sensor.maxTemp
    output_sensor["temperature"] = sensor.temperature
    output_sensor["minHumidity"] = sensor.minHumidity
    output_sensor["maxHumidity"] = sensor.maxHumidity
    output_sensor["humidity"] = sensor.humidity
    output_sensor["tempUnit"] = sensor.tempUnit
    
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

#region Main Routine
app.register_blueprint(swaggerui_blueprint)

#endregion


# Read the configuration file
# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config("/home/rod/Projects/Code/raspberry-pi-vivarium/src/api/config/config.json")

server = Server(config.Server.Host, config.Server.Port, config.Server.Debug)

# access elements
sensor_tempUnit = config.TempUnit
mode = config.Mode
pollFrequency = config.PollFrequency

vivaria = Vivaria(config.Vivaria.Title)

for viv in config.Vivaria.Vivarium:
  vivarium = Vivarium(viv['Name'], viv['Location'])

  for sensor in viv['Sensors']:
      port = sensor["Port"]
      sensorObj = Sensor(
          sensor["Name"],
          port,
          sensor["Pin"],
          sensor["SensorType"],
          sensor["Comment"],
          sensor["MinTemperature"],
          sensor["MaxTemperature"],
          sensor["MonitorTemperature"],
          sensor["MinHumidity"],
          sensor["MaxHumidity"],
          sensor["MonitorHumidity"],
          sensor_tempUnit
      )
      vivarium.sensors[str(port)] = sensorObj

vivaria.vivarium = vivarium

sensorReaderWorkerThread = SensorReaderProcess()
sensorReaderWorkerThread.start()

if __name__ == "__main__":
  app.run(host=server.host, port=server.port, debug=server.debug)