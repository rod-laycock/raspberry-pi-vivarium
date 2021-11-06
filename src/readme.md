Features:
  Alarm - makes a beep if something is wrong.
    Different kinds of beeps
      Long continuous (--------)= Temp too high / low
      Pulsed (-- -- -- --) = Humidity too high / low
      Pipped (. . . . . .) = Something else
  Can be acknowledged until it returns to normal operation
  Can be paused for time frame.


Structure:

  WebService
    Initialises, reading the config
    Startsup and performs polled monitoring
    Writes to logs / records history of sensors - need to configure a log so it self maintains
    REST - returns JSON
      Get: Sensors


  Website
    Configurable - can upload new content / images / etc - write it yourself
    uses AJAX to perform auto updates from the webservice