
import sys
import os
import cv2
import numpy as np
	
class Detector:
	def detect(self, src):
		raise NotImplementedError("Every Detector must implement the detect method.")


class CascadedDetector(Detector):

	def __init__(self, cascade_fn='/home/root/Interim/app/face_rec_model/haarcascade_frontalface_alt2.xml', scaleFactor=1.2, minNeighbors=5, minSize=(30,30)):
		filepath = '/home/root/Interim/app/face_rec_model/haarcascade_frontalface_alt2.xml'
		self.cascade = cv2.CascadeClassifier(filepath)
		self.scaleFactor = scaleFactor
		self.minNeighbors = minNeighbors
		self.minSize = minSize
	
	def detect(self, src):
		if np.ndim(src) == 3:
			src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		src = cv2.equalizeHist(src)
		rects = self.cascade.detectMultiScale(src, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors, minSize=self.minSize)
		if len(rects) == 0:
			return np.ndarray((0,))
		rects[:,2:] += rects[:,:2]
		return rects
