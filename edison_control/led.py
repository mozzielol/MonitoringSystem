
import mraa  

LED_GPIO = 13                  
led = mraa.Gpio(LED_GPIO) # Get the LED pin object
led.dir(mraa.DIR_OUT)     # Set the direction as output
led.write(0)
led_state = "OFF"

def switch_led():
    global led_state
    if led_state == "OFF":
        led.write(1)
        led_state = "ON"
    else:
        led.write(0)
        led_state = "OFF"
    

def get_led_state():
    global led_state
    return led_state