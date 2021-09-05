import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115(busnum=4)

GAIN = 1

adc.start_adc(0, gain=GAIN)
print("PGSparkLite-Pedal - Expression Pedal Calibrator")
print("-----------------------------------------------")
print("Move your expression pedal to the top and bottom of its range while we measure the voltage output for 20 seconds.")
print("")

max = 0
min = 0

start = time.time()
while (time.time() - start) <= 20.0:    
    value = adc.get_last_result()

    if value > max:
        max = value
    if value < max:
        if value < min or min == 0:
            min = value    

    print("Voltage is", value)
    time.sleep(0.5)

adc.stop_adc()

print("-----------------------------------------------")
print("Add the following values to the config.txt file")
print("-----------------------------------------------")
print("")
print("expression_max_voltage =", max)
print("expression_min_voltage =", min)