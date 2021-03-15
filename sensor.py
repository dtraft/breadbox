import logging
import smokesignal
import store
import random
import time
import threading

import board
import adafruit_si7021
 
# Create library object using our Bus I2C port
sensor = adafruit_si7021.SI7021(board.I2C())
 
def background():
    while True:
        # Get readings from sensor
        temperature = round(sensor.temperature * 1.8 + 32)
        humidity = round(sensor.relative_humidity)
        
        store.temperature = temperature
        store.humidity = humidity

        logging.info("Sensor reading: " + str(temperature) + "F, " + str(humidity) + "%")

        smokesignal.emit('sensor_reading', temperature=temperature, humidity=humidity)
        
        time.sleep(30)

sensors = threading.Thread(name='sensors', target=background)
sensors.setDaemon(True)
sensors.start() 


