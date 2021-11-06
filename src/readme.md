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



  Website
    Configurable - can upload new content / images / etc - write it yourself
    uses AJAX to perform auto updates from the webservice



