from lib.common import dict_amp_preset, dict_user_preset

class PedalState:
    def __init__(self):
        self.connected_to_server = False
        self.connected_to_amp = False
        self.displayed_preset = 1
        self.selected_preset = 0
        self.connection_attempts = 0
        self.preset_mode = dict_amp_preset
        self.displayed_chain_preset = 1
        self.selected_chain_preset = 0
        self.chain_presets = []
        self.bpm = 0
        self.name = None

    def get_selected_preset(self):
        if self.preset_mode == dict_amp_preset:
            return dict_amp_preset + str(self.selected_preset)
        else:
            return dict_user_preset + str(self.selected_chain_preset)