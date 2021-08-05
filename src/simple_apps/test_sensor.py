
import Adafruit_DHT
import time

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
POLL_FREQUENCY = 5.0

while True:
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
	localtime = time.strftime("%d/%m/%Y %I:%M:%S %p", time.localtime())

	if humidity is not None and temperature is not None:
		print("{0}: Temp={1:0.1f}*C Hunmidity={2:0.1f}%".format(localtime, temperature, humidity))
	else:
		print("Failed to retreive data from sensor")
	time.sleep(POLL_FREQUENCY)
