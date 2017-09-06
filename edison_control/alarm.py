import mraa
import time

buzPin = mraa.Gpio(4)
buzPin.dir(mraa.DIR_OUT)
buzPin.write(0)


alarm_state = "OFF"

def switch_alarm():
    global alarm_state
    if alarm_state == "OFF":
        buzPin.write(1)
        alarm_state = "ON"
    else:
        buzPin.write(0)
        alarm_state = "OFF"
    

def get_alarm_state():
    global alarm_state
    return alarm_state
