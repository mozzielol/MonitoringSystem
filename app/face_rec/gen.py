import cv2
import os
def generate(frame,dir_name,count):
    if dir_name!='None':
        face_cascade=cv2.CascadeClassifier('./app/cascades/haarcascade_frontalface_default.xml')

        filepath = './app/data/at/%s'%dir_name
        if os.path.isdir(filepath):
            pass
        else:
            os.mkdir(filepath) 

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            f=cv2.resize(gray[y:y+h,x:x+w],(200,200))
            cv2.imwrite('%s/%s.jpg'%(filepath,str(count)),f)
            print count
            return True
        return False
    else:
        pass
        

