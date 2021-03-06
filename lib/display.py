##############################################################################
# PGSparkLite Pedal - Display Drivers
#
# Currently only support is provided for an OLED SSD1306 display
# but this module could be expanded to support other i2c compatible displays
#
# Uses AdaFruit SSD1306 library
# https://github.com/adafruit/Adafruit_Python_SSD1306
#
##############################################################################

import os
import threading

import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont


class oled_display:

    def __init__(self, i2c_address, display_height):

        RST = None

        try:
            if display_height == 64:
                self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=i2c_address)
            else:
                self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) # 128 x 32

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

        self.status_font = ImageFont.truetype('{}/Winkle-Regular.ttf'.format(source_dir), 20)
        self.preset_font = ImageFont.truetype('{}/Winkle-Regular.ttf'.format(source_dir), 100)

    def clear_screen(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.disp.display()

    def display_status(self, status):
        job = threading.Thread(target=self._display_status,
                                 args=(status),
                                 daemon=True)
        job.start()  

    def _display_status(self, status):
        if self.last_text == status:
             return
        else:
            self.last_text = status

        self.clear_screen()
        self.draw.text((0, -2), status, font=self.status_font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def show_unselected_preset(self, preset):
        self.show_selected_preset(str(preset) + ' *')

    def show_selected_preset(self, preset):
        job = threading.Thread(target=self._show_selected_preset,
                                 args=(preset),
                                 daemon=True)
        job.start()  

    def _show_selected_preset(self, preset):
        preset_string = str(preset)

        if self.last_text == preset_string:
            return
        else:
           self.last_text = preset_string

        self.clear_screen()
        self.draw.text((0, -2), preset_string, font=self.preset_font, fill=255)
        self.disp.image(self.image)
        self.disp.display()
