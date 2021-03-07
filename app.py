##############################################################
# PGSparkLite Pedal
#
# Using a SocketIO session, read physical switches, update
# OLED display and LED On/Off indicators
#
##############################################################


import time
from signal import SIGINT, signal

import socketio
from gpiozero import LED, Button

from config import (delay_button_gpio, delay_led_gpio, display_height,
                    down_button_gpio, drive_button_gpio, drive_led_gpio, font,
                    i2c_address, mod_button_gpio, mod_led_gpio, preset_size,
                    select_button_gpio, socketio_url, status_size,
                    up_button_gpio)
from lib.common import (dict_change_preset, dict_connection_failed,
                        dict_connection_lost, dict_connection_message,
                        dict_connection_success, dict_delay, dict_drive,
                        dict_effect_type, dict_message, dict_mod, dict_Off,
                        dict_On, dict_pedal_config_request, dict_pedal_connect,
                        dict_pedal_status, dict_preset, dict_refresh_onoff,
                        dict_state, dict_toggle_effect_onoff,
                        dict_update_preset, dict_value)
from lib.display import oled_display
from lib.messages import (msg_booting, msg_disconnected, msg_is_amp_on,
                          msg_no_connection, msg_pgsparklite_ok)

########
# Setup
########

sio = socketio.Client()

display = oled_display(i2c_address, display_height, font, status_size, preset_size)

connected_to_server = False
connected_to_amp = False
displayed_preset = 1
selected_preset = 0
connection_attempts = 0

up_button = Button(pin=up_button_gpio)
down_button = Button(pin=down_button_gpio)
select_button = Button(pin=select_button_gpio)

drive_led = LED(pin=drive_led_gpio)
drive_button = Button(pin=drive_button_gpio)

delay_led = LED(pin=delay_led_gpio)
delay_button = Button(pin=delay_button_gpio)

mod_led = LED(pin=mod_led_gpio)
mod_button = Button(pin=mod_button_gpio)


####################
# Utility Functions
####################

def do_connect():
    sio.emit(dict_pedal_connect, {})


def keyboard_exit_handler(signal_received, frame):
    sio.disconnect()
    sio.wait()    


def toggle_led(effect_type, state):
    if effect_type == dict_drive:
        if state == dict_On:
            drive_led.on()
        elif state == dict_Off:
            drive_led.off()
    elif effect_type == dict_delay:
        if state == dict_On:
            delay_led.on()
        elif state == dict_Off:
            delay_led.off()
    elif effect_type == dict_mod:
        if state == dict_On:
            mod_led.on()
        elif state == dict_Off:
            mod_led.off()
    else:
        # Effect_type not currently supported
        pass        


###################
# Switch Functions
###################

def delay():
    pedal_toggle(dict_delay)


def down():
    select_preset(False)


def drive():
    pedal_toggle(dict_drive)


def mod():
    pedal_toggle(dict_mod)


def pedal_toggle(effect_type):
    sio.emit(dict_toggle_effect_onoff, {dict_effect_type: effect_type})


def preset_select(preset):
    sio.emit(dict_change_preset, {dict_preset: str(preset)})


def select():
    global displayed_preset
    global selected_preset

    if displayed_preset == selected_preset:
        return

    preset_select(displayed_preset-1)


def select_preset(up):
    global displayed_preset
    global selected_preset

    if displayed_preset == 4 and up == True:
        displayed_preset = 1
    elif displayed_preset == 1 and up == False:
        displayed_preset = 4
    elif up == True:
        displayed_preset += 1
    else:
        displayed_preset -= 1

    if displayed_preset == selected_preset:
        display.show_selected_preset(selected_preset)
    else:
        display.show_unselected_preset(displayed_preset)


def up():
    select_preset(True)


###########################
# Standard SocketIO Events
###########################

@sio.event
def connect():
    global connected_to_server
    connected_to_server = True


@sio.event
def connect_error():
    display.display_status(msg_no_connection)


@sio.event
def disconnect():
    display.display_status(msg_disconnected)


#############
# Callbacks
#############

@sio.on(dict_connection_lost)
def connection_lost(data):
    global connection_attempts
    global connected_to_amp

    connection_attempts = 1

    display.display_status(msg_is_amp_on + str(connection_attempts))

    connected_to_amp = False

    do_connect()


@sio.on(dict_connection_message)
def connection_message(data):
    # Listen for connection status messages
    global connected_to_amp
    global connection_attempts

    if data[dict_message] == dict_connection_success:
        connected_to_amp = True

        if connection_attempts > 0:
            sio.emit(dict_pedal_config_request,{})
            connection_attempts = 0

    elif data[dict_message] == dict_connection_failed:
        connection_attempts +=1
        display.display_status(msg_is_amp_on + str(connection_attempts))
        do_connect()    


@sio.on(dict_pedal_status)
def pedal_status(data):
    # Listen for Pedal status updates and update OLED/LEDs as necessary
    global selected_preset
    global displayed_preset

    selected_preset = int(data[dict_preset]) + 1
    displayed_preset = selected_preset    
    toggle_led(dict_drive, data[dict_drive])
    toggle_led(dict_delay, data[dict_delay])
    toggle_led(dict_mod, data[dict_mod])    

    display.show_selected_preset(selected_preset)


@sio.on(dict_refresh_onoff)
def refresh_onoff(data):
    # Listen for changes in On/Off state to update LEDs
    state = data[dict_state]
    effect_type = data[dict_effect_type]
    toggle_led(effect_type, state)    


@sio.on(dict_update_preset)
def update_preset_display(data):
    # Listen for change of Preset to update OLED screen
    global selected_preset
    selected_preset = int(data[dict_value]) + 1
    display.show_selected_preset(selected_preset)


if __name__ == '__main__':
    signal(SIGINT, keyboard_exit_handler)

    display.display_status(msg_booting)
    while not connected_to_server:
        try:
            sio.connect(socketio_url)
        except:            
            time.sleep(2)

    display.display_status(msg_pgsparklite_ok)

    # Connect the server to the amp
    do_connect()

    while not connected_to_amp:
        pass

    # Set up the footswitch functions
    up_button.when_pressed = up
    down_button.when_pressed = down
    select_button.when_pressed = select
    drive_button.when_pressed = drive
    delay_button.when_pressed = delay
    mod_button.when_pressed = mod
