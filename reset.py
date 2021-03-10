from waveshare_epd import epd4in2

epd = epd4in2.EPD()
print("Reseting display")
epd.init()
epd.Clear()
