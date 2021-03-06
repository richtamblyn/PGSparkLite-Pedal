###########################################################################
# PGSparkLite Pedal - Example Configuration File
#
# Copy this file to a new file called 'config.py'
# You can then make adjustments (if necessary) to that file without losing
# changes when updating the Pedal code.
###########################################################################

###########################################################################
# SocketIO URL
# Only change this line if you're hosting the PGSparkLite server somewhere
# other than the same Raspberry Pi Zero W as this code
###########################################################################

socketio_url = 'http://localhost:5000'

############################################################################
# OLED Display Address
# Change the line below to match the result of 'i2cdetect -y 1' (if not 3c)
############################################################################

i2c_address = 0x3C

####################################################################
# OLED Display Resolution
# Comment/uncomment the lines below to suit your display resolution
####################################################################

display_height = 64
# display_height = 32

################################
# Footswitches / LEDs
# Set the GPIO port assignments
################################

up_button_gpio = 16
down_button_gpio = 20
select_button_gpio = 21

drive_led_gpio = 26
drive_button_gpio = 5

delay_led_gpio = 12
delay_button_gpio = 6

mod_led_gpio = 19
mod_button_gpio = 13