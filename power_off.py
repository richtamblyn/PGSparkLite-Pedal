import config
from lib.display.display_server import DisplayServer
from lib.messages import msg_power_off

display = DisplayServer(config)

display.display_status(msg_power_off)

