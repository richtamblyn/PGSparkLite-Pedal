###########################################################################
# PGSparkLite Pedal - Example Configuration File
#
# Copy this file to a new file called 'config.py'
# You can then make adjustments (if necessary) to that file without losing
# changes when updating the Pedal code.
###########################################################################

###########################################################################
# SocketIO URL
# ------------
# Only change this line if you're hosting the PGSparkLite server somewhere
# other than the same Raspberry Pi Zero W as this code
###########################################################################

socketio_url = 'http://localhost:5000'

################################################################
# Display Model and Address
# -------------------------
# Change the line below to match the result of 'i2cdetect -y 1'
################################################################

model = 'SSD1306' #v1 Hardware
#model = 'HD44780' #v2 Hardware
i2c_address = 0x3C #Common address for OLED
#i2c_address = 0x27 #Common address for LCD
port_expander = 'PCF8574' #v2 Hardware only
#port_expander = 'MCP23008' #v2 Hardware only
#port_expander = 'MCP23017' #v2 Hardware only

####################################################################
# Display Resolution
# -----------------------
# Comment/uncomment the lines below to suit your display resolution
####################################################################

display_height = 64 #v1 Hardware
# display_height = 32 #v1 Hardware
# display_height = 4 #v2 Hardware
display_width = 20 #v2 Hardware only

###################################################################
# OLED TrueType Font
# ------------------
# Put a custom TTF font into /lib/fonts and update the line below
###################################################################

font = 'Nouveau_IBM.ttf'
status_size = 20
preset_size = 100

################################
# Footswitches / LEDs
# -------------------
# Set the GPIO port assignments
################################

up_button_gpio = 16
down_button_gpio = 20
select_button_gpio = 21

drive_led_gpio = 26
drive_button_gpio = 5

delay_led_gpio = 12
delay_button_gpio = 6

mod_led_gpio = 14 # We use this LED as a Power indicator until the code starts up.
mod_button_gpio = 13

# Optional switches (Hardware v2)
# reverb_led_gpio = 18
# reverb_button_gpio = 24
# preset_button_gpio = 23

############################
# Expression Pedal Support
# -------------------------
# Requires an ADS1115 board
############################

expression_pedal = False

# Voltage range can vary by pedal, adjust max and min
# to suit to make changes on the Spark more accurate
expression_max_voltage = 32767
expression_min_voltage = 10