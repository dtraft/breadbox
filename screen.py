import smokesignal
from threading import Timer

import display
import store
import relay


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

@smokesignal.on('sensor_reading')
@smokesignal.on('thermostat_updated')
@smokesignal.on('heating_updated')
@debounce(1)
def update_screen(**kwargs):
  global last_temperature
  global last_humidity
  global last_thermostat
  global last_heating
  
  if (last_temperature != store.temperature or
     last_humidity != store.humidity or
     last_thermostat != store.thermostat or 
     last_heating != relay.is_on()):

    display.render_screen_image(
      temperature=store.temperature,
      thermostat=store.thermostat,
      humidity=store.humidity,
      heating=relay.is_on()
    ).show()

  # Track lasts
  last_temperature = store.temperature
  last_humidity = store.humidity
  last_thermostat = store.thermostat
  last_heating = relay.is_on()