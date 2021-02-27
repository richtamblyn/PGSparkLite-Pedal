###########################################################################
# PGSparkLite Pedal - Example Configuration File
#
# Copy this file to a new file called 'config.py'
# You can then make adjustments (if necessary) to that file without losing
# changes when updating the Pedal code.
###########################################################################

##################################
# Enable debug logging to console
##################################

debug_mode = False

############################################################################
# OLED Display Address
# Change the line below to match the result of 'i2cdetect -y 1' (if not 3c)
############################################################################

i2c_address = 0x3C

####################################################################
# OLED Display Resolution
# Comment/uncomment the lines below to suit your display resolution
####################################################################

display_res = '128x64'
# display_res = '128x32'

################################
# Footswitches / LEDs
# Set the GPIO port assignments
################################

preset_1_button_gpio = 17
preset_2_button_gpio = 27
preset_3_button_gpio = 22
preset_4_button_gpio = 10

drive_led_gpio = 14
drive_button_gpio = 16

delay_led_gpio = 4
delay_button_gpio = 20

mod_led_gpio = 15
mod_button_gpio = 21

#####################################################################
# Time in seconds to wait before recognising a new change in a Pedal
#####################################################################

pedal_bounce_time = 2