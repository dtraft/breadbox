import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

channels = [14]

GPIO.setup(channels, GPIO.OUT)

GPIO.output(channels, GPIO.HIGH) 
