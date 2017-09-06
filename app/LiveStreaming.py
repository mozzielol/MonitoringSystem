import cv2
import time
from face_rec import recognizer
from FaceDetector import face_detector
#from FaceDetector import face_detector_service
from MotionDetector import motion_detector
from camera import VideoCamera as camera
from face_rec import gen
from flask import redirect
from face_rec_model.facerec.serialization import load_model
from face_rec_model.ExtendedPredictableModel import ExtendedPredictableModel
from face_rec_model import model_recognizer

def gen_normal():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        _,frame = cv2.imencode('.jpg',img)
        yield (b'--frame\r\n'
		   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
    cap.release()
        
def gen_face(name=None):
    cap = cv2.VideoCapture(0)
    count=0
    while count<20:
        success, img = cap.read()
        if name!='None':
            if gen.generate(img,name,count):
                count+=1
        _,frame = cv2.imencode('.jpg',img)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
    cap.release()    


def gen_detector():
    cap = cv2.VideoCapture(0)
    pre_time = time.time()
    while True:
        ret, background = cap.read()
        cur_time = time.time()
        if cur_time-pre_time>10:
            print 'begin'
            frame = cap.read()[1]
            pre_time = cur_time
            face_detector(frame).start()
            motion_detector(background,frame).start()

        _,web_frame = cv2.imencode('.jpg', background)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + web_frame.tobytes() + b'\r\n')
    cap.release()
        
def gen_recognizer():
    recognizer.face_rec()
    while True:
        frame = recognizer.get_frame()
        yield (b'--frame\r\n'
		   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    recognizer.release()

def gen_model_recognizer():
    Rec = model_recognizer.Rec()
    while True:
        frame = Rec.get_frame()
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

'''
def gen_service():
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        face_detector_service(img).start()
        _,frame = cv2.imencode('.jpg',img)
        yield (b'--frame\r\n'
		   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
    cap.release()
'''
