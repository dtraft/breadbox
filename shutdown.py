#!/usr/bin/env python3

from gpiozero import OutputDevice

from lib.waveshare_epd import epd4in2

import display

print("Handling shutdown")


epd = epd4in2.EPD()
epd.init()

image = display.render_welcome_screen()
epd.display(epd.getbuffer(image))
