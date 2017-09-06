#!/usr/bin/python


import mraa     # For accessing the GPIO
import time     # For sleeping between blinks
import threading


LED_GPIO = 13                  
blinkLed = mraa.Gpio(LED_GPIO) # Get the LED pin object
blinkLed.dir(mraa.DIR_OUT)     # Set the direction as output
ledState = False               # LED is off to begin with
blinkLed.write(0)
FLAG = True

class Blink_Led(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run():
        # One infinite loop coming up
        while check_flag():
            if ledState == False:
                # LED is off, turn it on
                blinkLed.write(1)
                ledState = True        # LED is on
            else:
                blinkLed.write(0)
                ledState = False

            # Wait for some time 
            time.sleep(1)

    def set_flag(self,flag):
        global FLAG
        FLAG = flag

    def check_flag(self):
        global FLAG
        return FLAG

