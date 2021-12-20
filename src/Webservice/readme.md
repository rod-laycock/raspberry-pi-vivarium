# Features
## Alarm
Makes a beep if something is wrong.

Different kinds of beeps
- Long continuous (--------)= Temp too high / low
- Pulsed (-- -- -- --) = Humidity too high / low
- Pipped (. . . . . .) = Something else
  
Can be acknowledged until it returns to normal operation, at which point it removes the acknowledgement
Can be paused for time frame.


# Structure:
## WebService
Initialises, reading the config
Startsup and performs polled monitoring
Writes to logs / records history of sensors - need to configure a log so it self maintains
REST - returns JSON
Runs on localhost:8080

## Website
Runs on localhost:80
Connects to localhost:8080 to get sensor data


### Sensors      
GET: /Sensor 
returns all sensor data

GET: /Sensor/Id
returns sensor data for the Id of the sensor specified in the Id
      
POST: Sensor/Id
Sets Sensor settings

### Alarms
POST: /Alarm/Id
Acknowledges an alarm - Id is the sensor Id

POST: /Alarm/Id/ISO_8601_DATE_TIME 
Suspends an alarm associated with Sensor Id, until a particular ISO DateTime


### Configuration
#### Current Configuration
GET: Config/Current
Returns the current config

POST: Config/Current
Sets the current config

#### Default / Factory reset configuration
GET: Config/Default
Returns the default config - factory settings

POST: Config/Default
Sets the default config

### Logs      
GET: Logs
returns all logs

GET: Logs/ISO_8601_DATE_TIME
returns all logs from ISO Date time until now

GET: Logs/ISO_8601_DATE_TIME/ISO_8601_DATE_TIME
returns all logs from ISO Date (1) time until ISO Date (2)

      
      
      Get: Sensors

To make a call to a JSON endpoint - dead easy

    import requests
    
    request = requests.get(url)
    json = request.json

    json.get("element")[index].get("element")



Throw exceptions

    raise ValueError("blah")


Website
    Configurable - can upload new content / images / etc - write it yourself
    uses AJAX to perform auto updates from the webservice



# Functionality Require
The following functionality is required
1. Read data from a sensor
2. Extend 1 sensor to multiple sensors
   1. Ability to move sensors around (the device will have plugs on the back to plug these into), so Sensor 1 may not be in plug 1
3. Ability to configure it via config file - this means we can amend stuff remotely /  web interface and when rebooting settings perist
   1. Read / Write to JSON config
4. Record history
   1. Need to record the history for X Days - again configurable
5. Take action
   1. Sound alarm - if installed
   2. Send email - if configured
   3. light / flash LED - if installed
      1. Change colour of LED
   4. Display on a screen - if installed
6. Ability to silence alarms
7. Ability to suspend alarms for a given time period
8. 