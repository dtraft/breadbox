#!/usr/bin/env python3

import time
import subprocess
from gpiozero import Button
from signal import pause

from lib.waveshare_epd import epd4in2

import display

print("Handling shutdown")

epd = epd4in2.EPD()
epd.init()
epd.Clear()

image = display.render_welcome_screen()
epd.display(epd.getbuffer(image))
