import time
import cv2
import threading
#from send_email import sender
import numpy as np
import random
import secret


MOTIONDETECTED = 'motion detected'
IMGPATH_MOTION = './app/img_detected/motion_image/'


class motion_detector(threading.Thread):
    def __init__(self,background,frame):
        self.background = background
        self.frame = frame
        threading.Thread.__init__(self)

    def run(self):
        global MOTIONDETECTED
        global IMGPATH_MOTION
        
        frame = self.frame
        background = self.background
        background_gray = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
        imgName = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
        __motionImage = IMGPATH_MOTION + '%s.png'%str(imgName)
        
        background_gray = cv2.GaussianBlur(background_gray, (21, 21), 0)
        
        
        frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (21, 21), 0)


        frameDelta = cv2.absdiff(background_gray, frame_gray)
        
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        
        for c in cnts:
            if cv2.contourArea(c)<500:
                continue
            (x,y,w,h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            imgName = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
            __motionImage = IMGPATH_MOTION +'%s.png'%str(imgName)
            cv2.imwrite(__motionImage,frame)
    
            if count == 0 and secret.emailstate_motion:
                secret.emailstate_motion = False
                #sender(__motionImage,MOTIONDETECTED).start()
                print 'motion'
                print 'sending'
                count+=1
