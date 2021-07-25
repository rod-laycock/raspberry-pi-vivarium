# raspi-vivarium
Raspberry Pi Vivarium monitoring / control project.

## Introduction
I have 4 ball pythons and need to check the temperature, humidity (during shedding), etc.  So this project will begin as a sumple temp/humidity recorder with web access and could build up to include web-cams, temperature controller, over / under temperature alarms, door open sensors, etc.

## Components Required
The following components, and a little skill will be required, please note I get most of my stuff from [The Pi Hut](https://thepihut.com/collections/raspberry-pi-store) but other parts are available from other stores (I have listed some of them in the Appendix):
- A Raspberry Pi 
- DHT11 or DHT22 temp/humidity probe
- 10K resistor
- wire
- soldering iron
- heat shrink
- IDE / PATA cable or 40-pin GPIO Ribbon Cable.

Depending on how many vivariums you want to monitor will denote the type you need, I'm going for a Raspberry Pi 4, because I have a couple spare.

The DHT11 is a cheap sensor, but the DHT22 is more precise and will last longer, your call which one to opt for.

For those young enough to not know what an IDE or PATA cable is, it's a 40 pin ribbon cable which used to connect hard disks to motherboards, we are using this to avoid soldering directly onto the Raspberry Pi's 40 pin extension slot (almost like these 2 were made for each other isn't it). 


# Appendix A - Shopping
Here are some stores to buy essentials from:

- [The Pi Hut](https://thepihut.com/collections/raspberry-pi-store) 
- [Pimori](https://shop.pimoroni.com/)
- [Amazon - of course](https://www.amazon.co.uk)
- [ebay](https://www.ebay.co.uk)
