import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22

SENSOR_LIST = {"Sensor 1": 4, "Sensor 2": 17}

POLL_FREQUENCY = 5.0

while True:
    for sensorName, sensorPin in SENSOR_LIST.items():
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, sensorPin)
        localtime = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime())

        if humidity is not None and temperature is not None:
            print(
                "{0} {1} Temp={2:0.1f}*C Hunmidity={3:0.1f}%".format(
                    localtime, sensorName, temperature, humidity
                )
            )
        else:
            print("Failed to retreive data from sensor")
    time.sleep(POLL_FREQUENCY)
