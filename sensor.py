import smokesignal
import store
import random
import time

import threading

def background():
    while True:
        # Get readings from sensor
        temperature = random.randint(79, 81)
        humidity = 45

        store.temperature = temperature
        store.humidity = humidity

        print("Sensor reading: " + str(temperature) + "F, " + str(humidity) + "%")

        smokesignal.emit('sensor_reading', temperature=temperature, humidity=humidity)
        
        time.sleep(15)

sensors = threading.Thread(name='sensors', target=background)
sensors.start()
    


