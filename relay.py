import smokesignal
import statistics
import store

last_five_readings = []
is_heating = False

def is_on():
  return is_heating

@smokesignal.on('sensor_reading')
def handle_sensor_reading(temperature, humidity):
  global last_five_readings
  last_five_readings.append(temperature)
  last_five_readings = last_five_readings[-5:]

  adjust_relay()

@smokesignal.on('thermostat_updated')
def handle_thermostat_updated(thermostat):
  adjust_relay()

def should_heat():
  return statistics.median(last_five_readings) < store.thermostat

def adjust_relay():
  global is_heating
  if should_heat() and not is_heating:
    print("Start heating (would change pin to HIGH)")
    is_heating = True
    smokesignal.emit('heating_updated', heating=is_heating)
  elif is_heating and not should_heat():
    print("End heating (would change pin to LOW)")
    is_heating = False
    smokesignal.emit('heating_updated', heating=is_heating)

