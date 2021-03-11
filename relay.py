from gpiozero import OutputDevice
import smokesignal
import statistics
import store

last_five_readings = []

relay = OutputDevice(14, active_high=False)

def is_on():
  return relay.value

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
  if should_heat() and not is_on():
    print("Starting heating")
    relay.on()
    smokesignal.emit('heating_updated', heating=is_on())
  elif is_on()  and not should_heat():
    print("Stopping heating")
    relay.off()
    smokesignal.emit('heating_updated', heating=is_on())

