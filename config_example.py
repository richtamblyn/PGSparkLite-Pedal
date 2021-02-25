###########################################################################
# PGSparkLite Pedal - Example Configuration File
#
# Copy this file to a new file called 'config.py'
# You can then make adjustments (if necessary) to that file without losing
# changes when updating the Pedal code.
###########################################################################

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

preset_1_button_gpio = 2
preset_2_button_gpio = 3
preset_3_button_gpio = 4
preset_4_button_gpio = 17

drive_led_gpio = 14
drive_button_gpio = 15

delay_led_gpio = 27
delay_button_gpio = 22

mod_led_gpio = 23
mod_button_gpio = 24