##############################################################
# PGSparkLite Pedal
#
# Using a SocketIO session, read physical switches, update
# OLED display and LED On/Off indicators
#
##############################################################


import socketio
from gpiozero import LED, Button

from config import (delay_button_gpio, delay_led_gpio, display_res,
                    drive_button_gpio, drive_led_gpio, i2c_address,
                    mod_button_gpio, mod_led_gpio, pedal_bounce_time,
                    preset_1_button_gpio, preset_2_button_gpio,
                    preset_3_button_gpio, preset_4_button_gpio, debug_mode)
from lib.common import (dict_change_preset, dict_connection_success,
                        dict_delay, dict_drive, dict_effect_type, dict_message,
                        dict_mod, dict_Off, dict_On, dict_preset, dict_state,
                        dict_toggle_effect_onoff)
from lib.display import oled_display

########
# Setup
########

sio = socketio.Client()

display = oled_display(i2c_address, display_res)

connected_to_server = False
connected_to_amp = False
selected_preset = 0

preset_1_button = Button(pin=preset_1_button_gpio,
                         bounce_time=pedal_bounce_time)
preset_2_button = Button(pin=preset_2_button_gpio,
                         bounce_time=pedal_bounce_time)
preset_3_button = Button(pin=preset_3_button_gpio,
                         bounce_time=pedal_bounce_time)
preset_4_button = Button(pin=preset_4_button_gpio,
                         bounce_time=pedal_bounce_time)

drive_led = LED(pin=drive_led_gpio)
drive_button = Button(pin=drive_button_gpio, bounce_time=pedal_bounce_time)

delay_led = LED(pin=delay_led_gpio)
delay_button = Button(pin=delay_button_gpio, bounce_time=pedal_bounce_time)

mod_led = LED(pin=mod_led_gpio)
mod_button = Button(pin=mod_button_gpio, bounce_time=pedal_bounce_time)


###################
# Switch Functions
###################

def pedal_toggle(button, effect_type=None):
    sio.emit(dict_toggle_effect_onoff, {dict_effect_type: effect_type})

    if debug_mode:
        print(effect_type + ' pressed. GPIO: ' + str(button.pin.number))


def preset_select(button, preset=None):
    sio.emit(dict_change_preset, {dict_preset: preset})

    if debug_mode:
        print('Preset ' + preset + ' pressed. GPIO:' + str(button.pin.number))


###########################
# Standard SocketIO Events
###########################

@sio.event
def connect():
    global connected_to_server
    connected_to_server = True
    display.display_status("Connected to PGSparkLite service...")


@sio.event
def connect_error():
    display.display_status("The connection failed!")


@sio.event
def disconnect():
    display.display_status("Disconnected.")


#############
# Callbacks
#############

@sio.on('connection-message')
def connection_message(data):
    # Listen for connection status messages
    global connected_to_amp

    display.display_status(data[dict_message])
    if data[dict_message] == dict_connection_success:
        connected_to_amp = True


@sio.on('pedal-status')
def pedal_status(data):
    # Listen for Pedal status updates and update OLED/LEDs as necessary
    global selected_preset
    selected_preset = int(data[dict_preset]) + 1
    display.show_selected_preset(str(selected_preset))

    toggle_led(dict_drive, data[dict_drive])
    toggle_led(dict_delay, data[dict_delay])
    toggle_led(dict_mod, data[dict_mod])

    if debug_mode:
        print(dict_preset + '' + data[dict_preset])
        print(dict_delay + ' ' + data[dict_delay])
        print(dict_drive + ' ' + data[dict_drive])
        print(dict_mod + ' ' + data[dict_mod])


@sio.on('refresh-onoff')
def refresh_onoff(data):
    # Listen for changes in On/Off state to update LEDs
    state = data[dict_state]
    effect_type = data[dict_effect_type]
    toggle_led(effect_type, state)

    if debug_mode:
        print(effect_type + ' ' + state)


@sio.on('update-preset')
def update_preset_display(data):
    # Listen for change of Preset to update OLED screen
    global selected_preset
    selected_preset = int(data['value']) + 1
    display.show_selected_preset(str(selected_preset))


####################
# Utility Functions
####################

def toggle_led(effect_type, state):
    if effect_type == dict_drive:
        if state == dict_On:
            drive_led.on
        elif state == dict_Off:
            drive_led.off
    elif effect_type == dict_delay:
        if state == dict_On:
            delay_led.on
        elif state == dict_Off:
            delay_led.off
    elif effect_type == dict_mod:
        if state == dict_On:
            mod_led.on
        elif state == dict_Off:
            mod_led.off
    else:
        if debug_mode:
            print('Effect_type not currently supported')


########################
# Main application loop
########################

if __name__ == '__main__':

    sio.connect('http://localhost:5000')

    while not connected_to_server:
        pass

    # Connect the server to the amp
    sio.emit('pedal_connect', {})

    while not connected_to_amp:
        pass

    # Setup the footswitch functions
    preset_1_button.when_pressed = preset_select(preset_1_button, preset='0')
    preset_2_button.when_pressed = preset_select(preset_2_button, preset='1')
    preset_3_button.when_pressed = preset_select(preset_3_button, preset='2')
    preset_4_button.when_pressed = preset_select(preset_4_button, preset='3')

    drive_button.when_pressed = pedal_toggle(
        drive_button, effect_type=dict_drive)
    delay_button.when_pressed = pedal_toggle(
        delay_button, effect_type=dict_delay)
    mod_button.when_pressed = pedal_toggle(mod_button, effect_type=dict_mod)
