#################################################
# PGSparkLite Pedal - OLED Display (v1 Hardware)
#################################################

import os

import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont


class SSD1306_Display:

    def __init__(self, i2c_address, display_height, font, status_size, preset_size):

        RST = None

        try:
            if display_height == 64:
                self.disp = Adafruit_SSD1306.SSD1306_128_64(
                    rst=RST, i2c_address=i2c_address)
            else:
                self.disp = Adafruit_SSD1306.SSD1306_128_32(
                    rst=RST)  # 128 x 32

            self.disp.begin()
            self.disp.clear()
            self.disp.display()

            self.last_text = ''
        except:
            print('ERROR: Could not connect to display')

        # Initialise the screen
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

        source_dir = os.path.dirname(os.path.realpath(__file__))

        font_path = source_dir + '/fonts/' + font

        self.status_font = ImageFont.truetype(font_path, status_size)
        self.preset_font = ImageFont.truetype(font_path, preset_size)

    def clear_screen(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.disp.display()

    def display_status(self, status):
        if self.last_text == status:
            return
        else:
            self.last_text = status

        self.clear_screen()
        self.draw.text((0, -2), status, font=self.status_font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def show_selected_preset(self, preset):
        if self.last_text == preset:
            return
        else:
            self.last_text = preset

        self.clear_screen()
        self.draw.text((0, -12), preset,
                       font=self.preset_font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def show_unselected_preset(self, preset):
        self.show_selected_preset(preset + '*')