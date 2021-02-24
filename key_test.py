##############################################################
# PGSparkLite Pedal - Keyboard Tester
# 
# Using a SocketIO session, use keyboard presses
# to change Spark 40 amp settings
#
# (NOTE: Must run under root on Linux platform)
#
##############################################################


import socketio
import keyboard
import time

sio = socketio.Client()

connected_to_amp = False


@sio.event
def connect():
    print("Connected to PGSparkLite service...")
    main_loop()


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("Disconnected.")


@sio.on('connection-message')
def connection_message(data):
    global connected_to_amp

    print(data['message'])
    if data['message'] == 'Connected.':
        connected_to_amp = True


def connect():
    sio.connect('http://localhost:5000')


def main_loop():
    global connected_to_amp

    # Constants
    amp = 'AMP'
    comp = 'COMP'
    delay = 'DELAY'
    drive = 'DRIVE'
    gate = 'GATE'
    reverb = 'REVERB'
    mod = 'MOD'
    effect_type = 'effect_type'
    change_preset = 'change_preset'
    toggle_effect_onoff = 'toggle_effect_onoff'

    # Connect the server to the amp
    sio.emit('pedal_connect', {})

    while not connected_to_amp:
        pass

    print('Ready for key input...')

    #########
    # TESTS 
    #########

    last_key = ''
    count = 0

    while True:     
        if count > 30 and last_key != '':
            print('Releasing ' + last_key)
            last_key = ''
            count = 0

        if keyboard.is_pressed('1'):
            if last_key == '1':
                pass
            else:
                last_key = '1'
                count = 0 
                sio.emit('change_preset', {'preset': '0'})
                print('Selected Preset 1')                        
        elif keyboard.is_pressed('2'):
            if last_key == '2':
                 pass
            else:
                last_key = '2'
                count = 0 
                sio.emit('change_preset', {'preset': '1'})
                print('Selected Preset 2')
        elif keyboard.is_pressed('3'):
            if last_key == '3':
                pass
            else:
                last_key = '3'
                count = 0 
                sio.emit('change_preset', {'preset': '2'})
                print('Selected Preset 3')
        elif keyboard.is_pressed('4'):
            if last_key == '4':
                pass
            else:
                last_key = '4'
                count = 0 
                sio.emit('change_preset', {'preset': '3'})
                print('Selected Preset 4')
        elif keyboard.is_pressed('o'):
            if last_key == 'o':
                pass
            else:
                last_key = 'o'
                count = 0 
                sio.emit(toggle_effect_onoff,{effect_type: drive})
                print('Toggling Drive Pedal')
        elif keyboard.is_pressed('m'):
            if last_key == 'm':
                pass
            else:
                last_key = 'm'
                count = 0 
                sio.emit(toggle_effect_onoff,{effect_type: mod})
                print('Toggling Mod Pedal')
        elif keyboard.is_pressed('d'):
            if last_key == 'd':
                pass
            else:
                last_key = 'd'
                count = 0 
                sio.emit(toggle_effect_onoff,{effect_type: delay})
                print('Toggling Delay Pedal')
        elif keyboard.is_pressed('q'):
            if last_key == 'q':
                pass
            else:
                last_key = 'q'
                count = 0 
                sio.emit('eject')
                print('Quitting Tester')
                break                

        count += 1
        time.sleep(0.2)

    sio.disconnect()

if __name__ == '__main__':
    connect()
