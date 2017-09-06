import sys
import time
import mraa
import pyupm_i2clcd as lcd
import threading

class lcdDisplay(threading.Thread):
    def __init__(self,message,color=(255,0,0),time_wait=10):
        threading.Thread.__init__(self)
        self.mLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
        self.mLcd.setCursor(0, 0)
        self.mLcd.setColor(color[0],color[1],color[2])
        self.message = message
        self.time_wait = time_wait
        
    def run(self):
        self.mLcd.write(self.message)
        time.sleep(self.time_wait)

