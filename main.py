from flask import Flask
import smokesignal

import store
import screen
import relay
import sensor

app = Flask(__name__,
            static_url_path='', 
            static_folder='static/dist')

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/api/readings')
def get_readings():
  return {
    'temperature': store.temperature,
    'humidity': store.humidity,
    'thermostat': store.thermostat,
    'heating': relay.is_on()
  }

@app.route('/api/thermostat/increment')
def increment_thermostat():
  store.thermostat += 1
  smokesignal.emit('thermostat_updated', thermostat=store.thermostat)
  return {
    'ok': True,
    'thermostat': store.thermostat
  }

@app.route('/api/thermostat/decrement')
def decrement_thermostat():
  store.thermostat -= 1
  smokesignal.emit('thermostat_updated', thermostat=store.thermostat)
  return {
    'ok': True,
    'thermostat': store.thermostat
  }

