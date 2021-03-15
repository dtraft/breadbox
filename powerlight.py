#!/usr/bin/python

import sys
import RPi.GPIO as GPIO

channel=15
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

command = sys.argv[1]

if command == "start":
    GPIO.output(channel, GPIO.LOW)
else:
    GPIO.output(channel, GPIO.HIGH)
    GPIO.cleanup()
