import cv2
import sys
import setlcd
from .. import secret
from helper.common import *
from helper.video import *
from facerec.serialization import load_model,save_model
from facerec.model import PredictableModel
from facedet.detector import CascadedDetector
from facerec.feature import Fisherfaces
from facerec.classifier import NearestNeighbor
from facerec.distance import EuclideanDistance
from ExtendedPredictableModel import ExtendedPredictableModel

def update():
    model_filepath='./app/data/at'
    model_filename='my_model.pkl'
    image_size=(200,200)
    [images, labels, subject_names] = read_images(model_filepath, image_size)
    list_of_labels = list(xrange(max(labels)+1))
    subject_dictionary = dict(zip(list_of_labels, subject_names))
    model = get_model(image_size=image_size, subject_names=subject_dictionary)
    model.compute(images, labels)
    save_model(model_filename, model)
    

def get_model(image_size, subject_names):
    """ This method returns the PredictableModel which is used to learn a model
        for possible further usage. If you want to define your own model, this
        is the method to return it from!
    """
    # Define the Fisherfaces Method as Feature Extraction method:
    feature = Fisherfaces()
    # Define a 1-NN classifier with Euclidean Distance:
    classifier = NearestNeighbor(dist_metric=EuclideanDistance(), k=1)
    # Return the model as the combination:
    return ExtendedPredictableModel(feature=feature, classifier=classifier, image_size=image_size, subject_names=subject_names)

def read_subject_names(path):
    """Reads the folders of a given directory, which are used to display some
        meaningful name instead of simply displaying a number.

    Args:
        path: Path to a folder with subfolders representing the subjects (persons).

    Returns:
        folder_names: The names of the folder, so you can display it in a prediction.
    """
    folder_names = []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            folder_names.append(subdirname)
    return folder_names

def read_images(path, image_size=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.

    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes 

    Returns:
        A list [X, y, folder_names]

            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
            folder_names: The names of the folder, so you can display it in a prediction.
    """
    c = 0
    X = []
    y = []
    folder_names = []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            folder_names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                if filename == '.DS_Store':
                    continue
                else:
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                        # resize to given size (if given)
                        if (image_size is not None):
                            im = cv2.resize(im, image_size)
                        X.append(np.asarray(im, dtype=np.uint8))
                        y.append(c)
                    except IOError, (errno, strerror):
                        print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
            c = c+1
    return [X,y,folder_names]


class Rec(object):
    def __init__(self, model=None, camera_id=0, cascade_filename='haarcascade_frontalface_alt2.xml'):
        update()
        self.model = load_model('my_model.pkl')
        self.detector = CascadedDetector(cascade_fn=cascade_filename, minNeighbors=5, scaleFactor=1.1)
        self.cam = create_capture(camera_id)
            
    def get_frame(self):
            ret, frame = self.cam.read()
            # Resize the frame to half the original size for speeding up the detection process:
            img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)
            imgout = img.copy()
            for i,r in enumerate(self.detector.detect(img)):
                x0,y0,x1,y1 = r
                # (1) Get face, (2) Convert to grayscale & (3) resize to image_size:
                face = img[y0:y1, x0:x1]
                face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, self.model.image_size, interpolation = cv2.INTER_CUBIC)
                # Get a prediction from the model:
                prediction = self.model.predict(face)[0]
                # Draw the face area in image:
                cv2.rectangle(imgout, (x0,y0),(x1,y1),(0,255,0),2)
                # Draw the predicted name (folder name...):
                draw_str(imgout, (x0-20,y0-20), self.model.subject_names[prediction])
                msg = 'Hello '+self.model.subject_names[prediction]
                if secret.face_flag:
                    setlcd.lcdDisplay(str(msg),(255,0,0)).start()
                    secret.face_flag=False
            _,webframe = cv2.imencode('.jpg',imgout) 
            return webframe.tobytes()
            
    def __del__(self):
        self.cam.release()

if __name__=='__main__':
    print Rec().get_frame()

            
