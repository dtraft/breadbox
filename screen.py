import smokesignal
from threading import Timer, Thread
from queue import Queue
import logging
from lib.waveshare_epd import epd4in2

import display
import store
import relay


screen_queue = Queue()

logging.info("Initializing e-ink display")
epd = epd4in2.EPD()
epd.init()
epd.Clear()


def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

last_temperature = store.temperature
last_humidity = store.humidity
last_thermostat = store.thermostat
last_heating = relay.is_on()

def screen_worker():
  while True:
    screen_data = screen_queue.get()
  
    image = display.render_screen_image(
      temperature=screen_data["temperature"],
      thermostat=screen_data["thermostat"],
      humidity=screen_data["humidity"],
      heating=screen_data["is_heating"]
    )
    epd.display(epd.getbuffer(image))
    
    screen_queue.task_done()

worker = Thread(target=screen_worker)
worker.setDaemon(True)
worker.start()

@smokesignal.on('sensor_reading')
@smokesignal.on('thermostat_updated')
@smokesignal.on('heating_updated')
@debounce(3)
def update_screen(**kwargs):
  global last_temperature
  global last_humidity
  global last_thermostat
  global last_heating
  
  if (last_temperature != store.temperature or
     last_humidity != store.humidity or
     last_thermostat != store.thermostat or 
     last_heating != relay.is_on()):

    screen_queue.put({
      "temperature": store.temperature,
      "humidity": store.humidity,
      "thermostat": store.thermostat,
      "is_heating": relay.is_on()
    })

      
  # Track last readings
  last_temperature = store.temperature
  last_humidity = store.humidity
  last_thermostat = store.thermostat
  last_heating = relay.is_on()
