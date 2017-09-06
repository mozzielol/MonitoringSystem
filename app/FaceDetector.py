import cv2
import time
import threading
from send_email import sender
import random
import secret
#from face_rec_service.client import FaceRecClient

FACEDETECTED = 'someone invade'
IMGPATH_FACE = './app/img_detected/invador/'
#IMGPATH_SERVICE = './app/face_rec_service/'
#SERVER_ADDRESS = "http://192.168.0.101:5000"


class face_detector(threading.Thread):
    def __init__(self,frame):
        self.frame = frame
        threading.Thread.__init__(self)

    def run(self):
        global FACEDETECTED
        global IMGPATH_FACE
        
        
        face_cascade=cv2.CascadeClassifier('./app/cascades/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)
        
        imgName = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
        for(x,y,w,h) in faces:
          cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
        if len(faces)>0:
          __faceimg = IMGPATH_FACE + '%s.png'%str(imgName)
          cv2.imwrite(__faceimg,self.frame)
          print "face"
          if secret.emailstate_face==True:
              sender(__faceimg,FACEDETECTED).start()
              secret.emailstate_face=False

class face_detector_service(threading.Thread):
    def __init__(self,frame):
        self.frame = frame
        threading.Thread.__init__(self)

    def run(self):
        global IMGPATH_SERVICE
        count=0
        face_cascade=cv2.CascadeClassifier('./app/cascades/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)
        
        for (x,y,w,h) in faces:
			f=cv2.resize(gray[y:y+h,x:x+w],(200,200))
		        cv2.imwrite('%sservice.jpg'%IMGPATH_SERVICE,f)
        faceRecClient = FaceRecClient(SERVER_ADDRESS)
        faceRecClient.recognize('%sservice.jpg'%IMGPATH_SERVICE)
