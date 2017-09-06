import cv2
import sys
import os

'''
usage: python generate.py directory_name

The directory_name is the label of the person(or the name of the person).
'''



def generate(dir_name):
	face_cascade=cv2.CascadeClassifier('../../cascades/haarcascade_frontalface_default.xml')
	camera = cv2.VideoCapture(0)
	count=0
	filepath = dir_name
	if os.path.isdir(filepath):
		pass
	else:
		os.mkdir(filepath) 
	while True:
		ret,frame=camera.read()
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces=face_cascade.detectMultiScale(gray,1.3,5)
		for (x,y,w,h) in faces:
			img = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			f=cv2.resize(gray[y:y+h,x:x+w],(200,200))
			cv2.imwrite('%s/%s.jpg'%(filepath,str(count)),f)
			count+=1
			print count

		cv2.imshow('camera',frame)
		if cv2.waitKey(1000/12) == ord('q'):
			break

	camera.release()
	cv2.destroyAllWindows()

if __name__=='__main__':
	generate(dir_name=sys.argv[1])