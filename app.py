##############################################################
# PGSparkLite Pedal
#
# Using a SocketIO session, read physical switches, update
# OLED display and LED On/Off indicators
#
##############################################################


import socketio
from gpiozero import LED, Button

from lib.common import (dict_change_preset, dict_connection_success,
                        dict_delay, dict_drive, dict_effect_type, dict_message,
                        dict_mod, dict_Off, dict_On, dict_preset, dict_state,
                        dict_toggle_effect_onoff)

########
# Setup
########

sio = socketio.Client()

connected_to_server = False
connected_to_amp = False
selected_preset = 0

preset_1_button = Button(2)
preset_2_button = Button(3)
preset_3_button = Button(4)
preset_4_button = Button(17)

drive_led = LED(14)
drive_button = Button(15)

delay_led = LED(27)
delay_button = Button(22)

mod_led = LED(23)
mod_button = Button(24)

###################
# Switch Functions
###################


def drive_pedal():
    sio.emit(dict_toggle_effect_onoff, {dict_effect_type: dict_drive})


def delay_pedal():
    sio.emit(dict_toggle_effect_onoff, {dict_effect_type: dict_delay})


def mod_pedal():
    sio.emit(dict_toggle_effect_onoff, {dict_effect_type: dict_mod})


def preset_1():
    sio.emit(dict_change_preset, {dict_preset: '0'})


def preset_2():
    sio.emit(dict_change_preset, {dict_preset: '1'})


def preset_3():
    sio.emit(dict_change_preset, {dict_preset: '2'})


def preset_4():
    sio.emit(dict_change_preset, {dict_preset: '3'})

###########################
# Standard SocketIO Events
###########################


@sio.event
def connect():
    global connected_to_server
    connected_to_server = True
    print("Connected to PGSparkLite service...")


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("Disconnected.")


#############
# Callbacks
#############

@sio.on('connection-message')
def connection_message(data):
    # Listen for connection status messages
    global connected_to_amp

    print(data[dict_message])
    if data[dict_message] == dict_connection_success:
        connected_to_amp = True


@sio.on('pedal-status')
def pedal_status(data):
    # Listen for Pedal status updates and update OLED/LEDs as necessary
    global selected_preset
    selected_preset = int(data[dict_preset]) + 1
    write_to_screen(str(selected_preset))

    toggle_led(dict_drive, data[dict_drive])
    toggle_led(dict_delay, data[dict_delay])
    toggle_led(dict_mod, data[dict_mod])


@sio.on('refresh-onoff')
def refresh_onoff(data):
    # Listen for changes in On/Off state to update LEDs
    state = data[dict_state]
    effect_type = data[dict_effect_type]
    toggle_led(effect_type, state)
    print(effect_type + ' ' + state)    


@sio.on('update-preset')
def update_preset_display(data):
    # Listen for change of Preset to update OLED screen
    global selected_preset
    selected_preset = int(data['value']) + 1
    write_to_screen(str(selected_preset))

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


def write_to_screen(message):    
    print(message)

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

    # Get the current

    preset_1_button.when_pressed = preset_1
    preset_2_button.when_pressed = preset_2
    preset_3_button.when_pressed = preset_3
    preset_4_button.when_pressed = preset_4

    drive_button.when_pressed = drive_pedal
    delay_button.when_pressed = delay_pedal
    mod_button.when_pressed = mod_pedal
