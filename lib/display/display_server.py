#######################################################
# Display Server - Handle multiple requests by queuing
#######################################################

import queue
import threading


class DisplayServer:
    def __init__(self, config):
        try:
            if config.model == 'SSD1306':
                # v1 Hardware
                from lib.display.ssd1306 import SSD1306_Display
                self.display = SSD1306_Display(config.i2c_address, config.display_height,
                                               config.font, config.status_size, config.preset_size)
            elif config.model == 'HD44780':
                # v2 Hardware
                from lib.display.hd44780 import HD44780_Display
                self.display = HD44780_Display(
                    config.i2c_address, config.port_expander, config.display_height, config.display_width)
        except:
            # Default to v1 OLED display
            print("Fallback to v1 OLED")
            from lib.display.ssd1306 import SSD1306_Display
            self.display = SSD1306_Display(config.i2c_address, config.display_height,
                                           config.font, config.status_size, config.preset_size)

        # Setup queue processor thread
        self.process_queue = queue.Queue()
        self.stopped=False
        threading.Thread(target=self.queue_processor, daemon=True).start()

    def stop(self):
        self.stopped=True

    def clear_screen(self):
        if self.stopped:
            return
        request = DisplayRequest('clear_screen', None)
        self.process_queue.put_nowait(request)

    def display_status(self, status):
        if self.stopped:
            return
        request = DisplayRequest('display_status', (status,))
        self.process_queue.put_nowait(request)

    def show_selected_preset(self, preset, name=None, bpm=None):
        if self.stopped:
            return
        request = DisplayRequest('show_selected_preset', (preset, name, bpm))
        self.process_queue.put_nowait(request)

    def show_unselected_preset(self, preset, name=None, bpm=None):
        if self.stopped:
            return
        request = DisplayRequest('show_unselected_preset', (preset, name, bpm))
        self.process_queue.put_nowait(request)

    def tap_mode(self, tempo):
        if self.stopped:
            return
        request = DisplayRequest('tap_mode', (tempo,))
        self.process_queue.put_nowait(request)

    def queue_processor(self):
        while True:
            request_item = self.process_queue.get(True)

            if request_item.type == 'clear_screen':
                self.display.clear_screen()
            elif request_item.type == 'display_status':
                self.display.display_status(request_item.params[0])
            elif request_item.type == 'show_selected_preset':
                self.display.show_selected_preset(
                    request_item.params[0], request_item.params[1], request_item.params[2])
            elif request_item.type == 'show_unselected_preset':
                self.display.show_unselected_preset(
                    request_item.params[0], request_item.params[1], request_item.params[2])
            elif request_item.type == 'tap_mode':
                self.display.tap_mode(request_item.params[0])
            elif request_item.type == 'update_bpm':
                self.display.update_bpm(request_item.params[0])

    def update_bpm(self, bpm):
        if self.stopped:
            return
        request = DisplayRequest('update_bpm', (bpm,))
        self.process_queue.put_nowait(request)


class DisplayRequest:
    def __init__(self, type, params):
        self.type = type
        self.params = params
