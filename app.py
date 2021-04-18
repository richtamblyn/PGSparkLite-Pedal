##############################################################
# PGSparkLite Pedal
#
# Using a SocketIO session, read physical switches, update
# OLED display and LED On/Off indicators
#
##############################################################


import os
import time
from datetime import datetime
from signal import SIGINT, signal

import requests
import socketio
from gpiozero import LED, Button

import config
from lib.common import (dict_amp_preset, dict_BPM, dict_chain_preset,
                        dict_change_preset, dict_connection_failed,
                        dict_connection_lost, dict_connection_message,
                        dict_connection_success, dict_delay, dict_drive,
                        dict_effect_type, dict_id, dict_message, dict_mod,
                        dict_name, dict_Name, dict_Off, dict_On,
                        dict_pedal_config_request, dict_pedal_connect,
                        dict_pedal_status, dict_preset, dict_preset_id,
                        dict_refresh_onoff, dict_reload_interface, dict_reverb,
                        dict_state, dict_toggle_effect_onoff,
                        dict_update_onoff, dict_update_preset,
                        dict_user_preset)
from lib.display.display_server import DisplayServer
from lib.messages import (msg_booting, msg_disconnected, msg_is_amp_on,
                          msg_no_connection, msg_pgsparklite_ok,
                          msg_shutting_down)
from lib.pedal_state import PedalState
from lib.tap_tempo import TapTempo

########
# Setup
########

sio = socketio.Client()

state = PedalState()

display = DisplayServer(config)

tap_tempo = TapTempo()

# Single touch to move up presets, hold for 2 seconds to change preset type
up_button = Button(pin=config.up_button_gpio, hold_time=2)

# Single touch to move down presets, hold for 2 seconds to enable tap tempo mode
down_button = Button(pin=config.down_button_gpio, hold_time=2)

# Single touch to select preset or if tap_mode, send tap tempo to the amp
select_button = Button(pin=config.select_button_gpio)

#Single touch to turn drive pedal on/off
drive_button = Button(pin=config.drive_button_gpio)
drive_led = LED(pin=config.drive_led_gpio)

# Single touch to turn delay pedal on/off
delay_button = Button(pin=config.delay_button_gpio)
delay_led = LED(pin=config.delay_led_gpio)

mod_led = LED(pin=config.mod_led_gpio)

# Single touch to turn mod pedal on/off, hold for 5 seconds to shutdown the pedal
mod_button = Button(pin=config.mod_button_gpio, hold_time=5)

# Test for optional reverb switch and LED (Hardware v2)
try:    
    # Single touch to turn reverb pedal on/off
    reverb_button = Button(pin=config.reverb_button_gpio)

    # Single touch to change preset type
    preset_button = Button(pin=config.preset_button_gpio)

    reverb_led = LED(pin=config.reverb_led_gpio)
except:
    reverb_led = None
    reverb_button = None
    preset_button = None


####################
# Utility Functions
####################

def clean_exit():
    drive_led.on()
    delay_led.on()
    mod_led.on()
    display.clear_screen()


def do_connect():
    sio.emit(dict_pedal_connect, {})


def get_user_presets():
    request = requests.get(config.socketio_url + '/chainpreset/getlist')
    return request.json()


def get_user_preset_index(id):
    global state

    count = 0

    chain_preset_count = len(state.chain_presets)

    if chain_preset_count == 0 or id > chain_preset_count:
        # Populate the pedal state
        state.chain_presets = get_user_presets()

    for preset in state.chain_presets:
        if preset[dict_id] == id:
            return count

        count +=1


def keyboard_exit_handler(signal_received, frame):
    sio.disconnect()
    sio.wait()
    clean_exit()


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
    elif effect_type == dict_reverb and reverb_led != None:
        if state == dict_On:
            reverb_led.on()
        elif state == dict_Off:
            reverb_led.off()
    else:
        # Effect_type not currently supported
        pass


###################
# Switch Functions
###################

def change_preset_type():
    global state

    if state.preset_mode == dict_amp_preset:
        state.chain_presets = get_user_presets()

        if len(state.chain_presets) == 0:
            # User does not have any custom presets currently
            return

        state.preset_mode = dict_user_preset        
        
        name = state.chain_presets[state.displayed_chain_preset-1][dict_name]

        display.show_unselected_preset(
            dict_user_preset + str(state.displayed_chain_preset), name)
    else:
        state.preset_mode = dict_amp_preset
        display.show_unselected_preset(
            dict_amp_preset + str(state.displayed_preset))


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


def reverb():
    pedal_toggle(dict_reverb)


def select():
    global tap_tempo

    if tap_tempo.enabled:
        tap_off()
    else:        
        global state

        if state.preset_mode == dict_amp_preset:
            preset_select(state.displayed_preset-1)
            state.selected_chain_preset = 0
        else:
            preset = state.chain_presets[state.displayed_chain_preset-1]
            data = {dict_preset_id: preset[dict_id]}
            requests.post(url=config.socketio_url, data=data)

            # Update other clients of our change
            sio.emit(dict_reload_interface, data)
            sio.emit(dict_pedal_config_request, {})

            state.selected_chain_preset = state.displayed_chain_preset
            state.selected_preset = 0

            display.show_selected_preset(state.get_selected_preset())


def select_preset(up):
    global state

    if state.preset_mode == dict_amp_preset:
        if state.displayed_preset == 4 and up == True:
            state.displayed_preset = 1
        elif state.displayed_preset == 1 and up == False:
            state.displayed_preset = 4
        elif up == True:
            state.displayed_preset += 1
        else:
            state.displayed_preset -= 1

        if state.displayed_preset == state.selected_preset:
            display.show_selected_preset(
                dict_amp_preset + str(state.selected_preset), state.name, state.bpm
            )
        else:
            display.show_unselected_preset(
                dict_amp_preset + str(state.displayed_preset)
            )
    else:
        chain_preset_count = len(state.chain_presets)

        if state.displayed_chain_preset == chain_preset_count and up == True:
            state.displayed_chain_preset = 1
        elif state.displayed_chain_preset == 1 and up == False:
            state.displayed_chain_preset = chain_preset_count
        elif up == True:
            state.displayed_chain_preset += 1
        else:
            state.displayed_chain_preset -= 1

        name = state.chain_presets[state.displayed_chain_preset-1][dict_name]

        if state.displayed_chain_preset == state.selected_chain_preset:
            display.show_selected_preset(
                dict_user_preset + str(state.selected_chain_preset), name, state.bpm
            )
        else:
            display.show_unselected_preset(
                dict_user_preset + str(state.displayed_chain_preset), name
            )


def shutdown():
    display.display_status(msg_shutting_down)
    os.system('sudo shutdown -h now')


def tap_on():
    global tap_tempo
    global state

    tap_tempo.enable(state.bpm)

    display.tap_mode(tap_tempo.tempo)


def tap_off():
    global tap_tempo
    tap_tempo.disable()

    #TODO: Send the tempo to the pedal
    print(tap_tempo.tempo)

    #TODO: Reset the screen


def up():
    global tap_tempo

    if tap_tempo.enabled:
        tap_tempo.tap()
        display.tap_mode(tap_tempo.tempo)
    else:
        select_preset(True)


###########################
# Standard SocketIO Events
###########################

@sio.event
def connect():
    global state
    state.connected_to_server = True


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
    global state

    state.connection_attempts = 1

    display.display_status(msg_is_amp_on + str(state.connection_attempts))

    state.connected_to_amp = False

    do_connect()


@sio.on(dict_connection_message)
def connection_message(data):
    # Listen for connection status messages
    global state

    if data[dict_message] == dict_connection_success:
        state.connected_to_amp = True

        if state.connection_attempts > 0:
            sio.emit(dict_pedal_config_request, {})
            state.connection_attempts = 0

    elif data[dict_message] == dict_connection_failed:
        state.connection_attempts += 1
        display.display_status(msg_is_amp_on + str(state.connection_attempts))
        do_connect()


@sio.on(dict_pedal_status)
def pedal_status(data):
    # Listen for status updates from the Amp or Interface and update OLED/LEDs as necessary
    global state
    
    if data[dict_chain_preset] != 0:
        state.preset_mode = dict_user_preset
        state.selected_chain_preset = get_user_preset_index(data[dict_chain_preset]) + 1
        state.displayed_chain_preset = state.selected_chain_preset
    else:
        state.preset_mode = dict_amp_preset
        state.selected_preset = int(data[dict_preset]) + 1
        state.displayed_preset = state.selected_preset

    state.bpm = data[dict_BPM]
    state.name = data[dict_Name]

    display.show_selected_preset(state.get_selected_preset(), name = state.name, bpm = state.bpm)

    toggle_led(dict_drive, data[dict_drive])
    toggle_led(dict_delay, data[dict_delay])
    toggle_led(dict_mod, data[dict_mod])
    toggle_led(dict_reverb, data[dict_reverb])    


@sio.on(dict_refresh_onoff)
def refresh_onoff(data):
    # Listen for changes in On/Off state to update LEDs
    toggle_led(data[dict_effect_type], data[dict_state])


@sio.on(dict_update_onoff)
def update_onoff(data):
    # Listen for Delay / Mod / Reverb knob changes on the Amp
    toggle_led(data[dict_effect_type], data[dict_state])


@sio.on(dict_update_preset)
def update_preset_display(data):
    # We no longer process this update and instead wait for the status
    # of the pedals before changing the display and LED states.
    pass
    

if __name__ == '__main__':
    signal(SIGINT, keyboard_exit_handler)

    display.display_status(msg_booting)
    while not state.connected_to_server:
        try:
            sio.connect(config.socketio_url)
        except:
            time.sleep(2)

    display.display_status(msg_pgsparklite_ok)

    # Connect the server to the amp
    do_connect()

    while not state.connected_to_amp:
        pass

    # Set up the footswitch functions
    up_button.when_pressed = up    

    down_button.when_pressed = down
    down_button.when_held = tap_on

    select_button.when_pressed = select

    drive_button.when_pressed = drive

    delay_button.when_pressed = delay

    mod_button.when_pressed = mod
    mod_button.when_held = shutdown

    if reverb_button != None:
        reverb_button.when_pressed = reverb

    if preset_button != None:
        preset_button.when_pressed = change_preset_type
    else:
        up_button.when_held = change_preset_type        

    sio.wait()

    clean_exit()
