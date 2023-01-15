####################################################
# PGSparkLite Pedal - HD44780 Display (v2 Hardware)
####################################################

from RPLCD.i2c import CharLCD
from lib.display.hd44780_large_font import HD44780_Large_Font


class HD44780_Display:
    def __init__(self, i2c_address, port_expander, display_height, display_width):

        self.lcd = CharLCD(port_expander, i2c_address, cols=display_width,
                           rows=display_height, auto_linebreaks=True)

        self.big_font = HD44780_Large_Font(self.lcd)

        self.last_cache = None

    def clear_screen(self):
        self.lcd.clear()

    def display_status(self, status):
        self.last_cache = None
        self.lcd.clear()
        self.lcd.write_string(status)

    def show_selected_preset(self, preset, name=None, bpm=None):
        if self.last_cache == (preset, name, bpm):
            return
        else:
            self.last_cache = (preset, name, bpm)

        self.lcd.clear()
        self.big_font.write_string(preset)
        self.lcd.cursor_pos = (3, 0)

        if name != None:
            if len(name) > 20:
                name = name[:17] + '...'

            self.lcd.write_string(name)

        if bpm != None:
            self.lcd.cursor_pos = (0, 13)
            self.lcd.write_string('BPM:' + str(bpm))

    def show_unselected_preset(self, preset, name=None, bpm=None):
        preset = preset + '*'
        self.show_selected_preset(preset, name, bpm)

    def tap_mode(self, tempo):
        if self.last_cache == tempo:
            return
        else:
            self.last_cache = tempo

        self.lcd.clear()
        self.big_font.write_string("{:.0f}".format(tempo))

        self.lcd.cursor_pos = (3, 0)
        self.lcd.write_string('Tap Tempo')

    def update_bpm(self, bpm):
        if bpm != None:
            self.lcd.cursor_pos = (0, 13)
            str_bpm=str(bpm)
            if len(str_bpm==2):
                str_bpm+=' '
            self.lcd.write_string('BPM:' + str_bpm)
