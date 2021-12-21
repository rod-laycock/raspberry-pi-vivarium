from threading import Thread
import time
from Models.SensorReader import SensorReader

class Worker(Thread):

    sensors = {}

    def __init__(self, sensors, date_time_format, poll_frequency):
        ''' Constructor. '''
 
        Thread.__init__(self)
        self.sensors = sensors
        self.date_time_format = date_time_format
        self.poll_frequency = poll_frequency
 
 
    def run(self):
      while True:
        for sensorPort in self.sensors:
            if sensorPort != None:
                sensor = self.sensors[sensorPort]
                dateTime, humidity, temperature = SensorReader.Read_Values(sensor)
                localtime = time.strftime(self.date_time_format, dateTime)

                if humidity is not None and temperature is not None:
                    sensor.temperature = temperature
                    sensor.humidity = humidity
                    # print("{1}: {0} Temp={2:0.1f}*C Hunmidity={3:0.1f}%".format(sensor.name, localtime, temperature, humidity))
                else:
                    sensor.temperature = 0
                    sensor.humidity = 0
            time.sleep(self.poll_frequency)