from config import font, i2c_address, preset_size, status_size, display_height
from lib.display import oled_display
from lib.messages import msg_power_off

display = oled_display(i2c_address, display_height, font, status_size, preset_size)

display.display_status(msg_power_off)

