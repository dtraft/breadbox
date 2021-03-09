import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', "Roboto.ttf")
welcome_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'images', "breadbox.xbm")

# get a font
label_font = ImageFont.truetype(font_path, 18)
label2_font = ImageFont.truetype(font_path, 16)
label3_font = ImageFont.truetype(font_path, 12)
unit_font = ImageFont.truetype(font_path, 72)
large_font = ImageFont.truetype(font_path, 54)

def render_screen_image(temperature, thermostat, humidity, heating):
  # create an image
  out = Image.new('1', (400, 300), 255)

  

  # get a drawing context
  draw = ImageDraw.Draw(out)

  # Temp
  draw.text((15,15), "Temperature", font=label_font, fill=0, anchor="lt")

  draw.regular_polygon(((90, 85), 30), n_sides=3, fill=0 if heating else 1, outline=0, rotation=0)
  
  if heating:
    draw.text((90, 110), "Heating", font=label2_font, fill=0, anchor="mt")

  draw.text((270, 90), str(temperature) + chr(176), font=unit_font, fill=0, anchor="rs")
  draw.line((300, 40, 215, 130), fill=0, width=2)
  draw.text((265, 80), str(thermostat) + chr(176), font=unit_font, fill=0, anchor="lt")

  # Divider
  draw.line((0, 150, 400, 150), fill=0, width=2)

  # Humidity
  draw.text((15,165), "Humidity", font=label_font, fill=0, anchor="lt")
  draw.text((115, 205), str(humidity) + "%", font=unit_font, fill=0, anchor="mt")

  # Last Update
  draw.text((385, 270), "Last Update", font=label3_font, fill=0, anchor="rs")
  draw.text((385, 285), datetime.now().strftime("%B %-d @ %-I:%M %p"), font=label3_font, fill=0, anchor="rs")

  return out


def render_welcome_screen():
  out = Image.new('1', (400, 300), 255)

  bmp = Image.open(welcome_image_path)
  out.paste(bmp, (20,65))

  return out

def render_goodbye_screen():
  out = Image.new('1', (400, 300), 255)
  # get a drawing context
  draw = ImageDraw.Draw(out)
  
  draw.text((200,150), "Happy Baking!", font=large_font, fill=0, anchor="mm")

  return out