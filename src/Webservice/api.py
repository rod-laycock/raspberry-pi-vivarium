from flask import Flask
from flask_restful import Resource, Api
import json
from distutils.util import strtobool

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    # Defaults
    server_host = "127.0.0.1"
    server_port = 5000
    server_debug = False

    # read file
    with open('Config/config.json', 'r') as configFile:
        configData = configFile.read()
    # parse file
    config = json.loads(configData)

    if ('Server' in config):
        if ('Host' in config['Server']):
            server_host = config['Server']['Host']

        if ('Port' in config['Server']):
            server_port = config['Server']['Port']
        
        if ('Debug' in config['Server']):
            server_debug = bool(strtobool(config['Server']['Debug']))

    app.run(debug=bool(server_debug), host=server_host, port=server_port)