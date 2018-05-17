# Bio Sensors, URC 2018
Sensors configured: DS18B20, DHT11 and MQ4.

* [MQ4_R0.ino](./MQ4_R0.ino) is used to find the R0 value for the MQ4 sensor
* [MQ4_ppmlog.ino](./MQ4_ppmlog.ino) is used to obtain ppm log readings from MQ4 sensor
* [DS18B20.ino](./DS18B20.ino) contains code to get temperature readings from DS18B20 sensor
> Needs OneWire and Dallas Temperature Sensor libraries. Just download and paste them in `/opt/arduino_{}/libraries`
* [DHT11_test.ino](./DHT11_test.ino) contains code for DHT11 sensor indiv. test
> Requires [Adafruit libraries](https://learn.adafruit.com/dht/using-a-dhtxx-sensor) for DHT11 since the normal ones don't work with Due.
* [Sensors.ino](./Sensors.ino) contains code for interfacing all the sensors in one
* [ROS_integ.py](./ROS_integ.py) communicates with the due and interfaces it with ROS