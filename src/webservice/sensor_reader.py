import threading
from models.sensor import Sensor


class SensorReaderProcess(threading.Thread):
    def __init__(self, sensor: Sensor):
        threading.Thread.__init__(self)
        self.sensor = sensor

        # helper function to execute the threads

    def run(self):
        print(str(self.thread_name) + " " + str(self.thread_ID))
