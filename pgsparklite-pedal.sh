#!/usr/bin/env bash

# Really simple startup script to start the PGSparkLite-Pedal client
# Just make it executable and run it on startup
# Whilst this will probably meet most users requirements, I recommend using Supervisor for better resilience

# Adjust this directory depending on your install directory
cd /home/pi/PGSparkLite-Pedal

python3 app.py