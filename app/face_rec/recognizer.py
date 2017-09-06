import cv2
import numpy as np
import sys
import os
import time
from .. import secret
import setlcd

def read_images(path,sz=None):
	global starttime
	starttime = time.time()
	print 'start time is ----->'+str(starttime)
	c=0
	X,y,folder_name = [],[],[]
	for dirname,dirnames,filenames in os.walk(path):
		print "dirname",dirname
		print "dirnames",dirnames
		print "filenames",filenames
		for subdirname in dirnames:
			folder_name.append(subdirname)
			print "subdirname",subdirname
			subject_path = os.path.join(dirname,subdirname)
			print "subject_path",subject_path
			for filename in os.listdir(subject_path):
				try:
					if(filename == ".directory"):
						continue
					filepath = os.path.join(subject_path,filename)
					im = cv2.imread(os.path.join(subject_path,filename),cv2.IMREAD_GRAYSCALE)

					if (sz is not None):
						im = cv2.resize(im,(200,200))
					X.append(np.asarray(im,dtype=np.uint8))
					y.append(c)
				except IOError,(errno,strerror):
					print "I/O error({0}):{1}".format(errno,strerror)
				except:
					print "error"
					raise
			c+=1
		
	return [X,y,folder_name]

def face_rec():
	global model
	global camera
	global names

	camera = cv2.VideoCapture(0)
	

	[X,y,names] = read_images('/home/root/Interim/app/data/at')
	y = np.asarray(y,dtype=np.int32)

	if len(sys.argv) == 3:
		out_dir = sys.argv[2]

	model = cv2.createEigenFaceRecognizer()
	model.train(np.asarray(X),np.asarray(y))
	
	
def get_frame():
	global camera
	global model
	global names
	flag = True
	face_cascade = cv2.CascadeClassifier('/home/root/Interim/app/cascades/haarcascade_frontalface_default.xml')
	read,img = camera.read()
	faces = face_cascade.detectMultiScale(img,1.3,5)
	for(x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		roi = gray[x:x+w,y:y+h]
		try:
			roi = cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
			params = model.predict(roi)
			print "Label:%s,Confidence:%.2f"%(params[0],params[1])
			cv2.putText(img,names[params[0]],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
			if params[1] > 4000:
				rectime = time.time()
				print 'rec time is -------' +str(rectime)
				
	                msg = 'Hello '+names[params[0]]
                        if secret.face_flag:
               		     setlcd.lcdDisplay(str(msg),(255,0,0)).start()
                             secret.face_flag=False
		except:
			continue
	ret, jpeg = cv2.imencode('.jpg', img)
	return jpeg.tobytes()
	
def release():
	camera.release()












