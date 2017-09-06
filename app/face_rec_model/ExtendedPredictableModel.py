from facerec.model import PredictableModel

class ExtendedPredictableModel(PredictableModel):


    def __init__(self, feature, classifier, image_size, subject_names):
        PredictableModel.__init__(self, feature=feature, classifier=classifier)
        self.image_size = image_size
        self.subject_names = subject_names