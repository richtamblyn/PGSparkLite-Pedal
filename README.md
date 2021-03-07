# PGSparkLite Pedal

This project extends the functionality of the PGSparkLite web interface (https://github.com/richtamblyn/PGSparkLite) to allow control of a Positive Grid Spark 40 amp using physical footswitches, On/Off status LEDs and an OLED display.

![PGSparkLite Pedal Prototype](https://richtamblyn.co.uk/wp-content/uploads/2021/03/IMG-5008-scaled.jpg)

## Current Features

- Amp Preset selection footswitches - Use Up/Down switches to move through amp presets 1-4 and hit Select switch to change.
- Dedicated Drive Pedal On/Off footswitch and LED indicator
- Dedicated Delay Pedal On/Off footswitch and LED indicator
- Dedicated Modulation Pedal On/Off footswitch and LED indicator
- Press the Modulation Pedal footswitch for 5 seconds to nicely shutdown the pedal.
- OLED Display - Shows status messages and selected Amp Preset

## Getting Started

- The PGSparkLite Pedal requires a brain. In this case, a Raspberry Pi Zero W and the PGSparkLite web interface installed. Follow the instructions here (if you haven't already) - https://github.com/richtamblyn/PGSparkLite/wiki/How-to-setup-a-Raspberry-Pi-Zero-W-and-PGSparkLite-from-scratch

- The recommended hardware list and wiring guide can be found here - https://github.com/richtamblyn/PGSparkLite-Pedal/wiki/Hardware-Recommendations-and-Wiring-Guide

- The software installation for PGSparkLite Pedal is documented in the Wiki here - https://github.com/richtamblyn/PGSparkLite-Pedal/wiki/How-to-install-and-configure-PGSparkLite-Pedal-software

- Finally, once you've got your pedal built and the software configured, a user guide for it all can be found here - https://github.com/richtamblyn/PGSparkLite-Pedal/wiki/PGSparkLite-Pedal---User-Guide

## Architecture

The PGSparkLite web interface and PGSparkLite-Pedal code take the place of the official Positive Grid mobile app. 

They allow the user to communicate with their Spark 40 amp via a web browser over WiFi or using physical footswitches attached to the GPIO of the Raspberry Pi Zero W host. Regardless of how it receives a message, PGSparkLite communicates to the amp using BlueTooth.

![PGSparkLite_Pedal_Comms](https://richtamblyn.co.uk/wp-content/uploads/2021/03/Pedal_Architecture.jpg)

## Future Development Ideas

- Long press Select switch to toggle Up/Down switches to step through user Chain Presets / Amp Presets
