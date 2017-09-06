
import numpy as np

class AbstractDistance(object):
    def __init__(self, name):
        self._name = name
        
    def __call__(self,p,q):
        raise NotImplementedError("Every AbstractDistance must implement the __call__ method.")
        
    @property
    def name(self):
        return self._name

    def __repr__(self):
        return self._name
        
class EuclideanDistance(AbstractDistance):
    def __init__(self):
        AbstractDistance.__init__(self,"EuclideanDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sqrt(np.sum(np.power((p-q),2)))

class CosineDistance(AbstractDistance):
  
    def __init__(self):
        AbstractDistance.__init__(self,"CosineDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return -np.dot(p.T,q) / (np.sqrt(np.dot(p,p.T)*np.dot(q,q.T)))

class NormalizedCorrelation(AbstractDistance):

    def __init__(self):
        AbstractDistance.__init__(self,"NormalizedCorrelation")
    
    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        pmu = p.mean()
        qmu = q.mean()
        pm = p - pmu
        qm = q - qmu
        return 1.0 - (np.dot(pm, qm) / (np.sqrt(np.dot(pm, pm)) * np.sqrt(np.dot(qm, qm))))
        
class ChiSquareDistance(AbstractDistance):

    def __init__(self):
        AbstractDistance.__init__(self,"ChiSquareDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        bin_dists = (p-q)**2 / (p+q+np.finfo('float').eps)
        return np.sum(bin_dists)

class HistogramIntersection(AbstractDistance):
    def __init__(self):
        AbstractDistance.__init__(self,"HistogramIntersection")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        return np.sum(np.minimum(p,q))

class BinRatioDistance(AbstractDistance):

    def __init__(self):
        AbstractDistance.__init__(self,"BinRatioDistance")

    def __call__(self, p, q):
        p = np.asarray(p).flatten()
        q = np.asarray(q).flatten()
        a = np.abs(1-np.dot(p,q.T)) # NumPy needs np.dot instead of * for reducing to tensor
        b = ((p-q)**2 + 2*a*(p*q))/((p+q)**2+np.finfo('float').eps)
        return np.abs(np.sum(b))

class L1BinRatioDistance(AbstractDistance):
  
    def __init__(self):
        AbstractDistance.__init__(self,"L1-BinRatioDistance")
    
    def __call__(self, p, q):
        p = np.asarray(p, dtype=np.float).flatten()
        q = np.asarray(q, dtype=np.float).flatten()
        a = np.abs(1-np.dot(p,q.T)) # NumPy needs np.dot instead of * for reducing to tensor
        b = ((p-q)**2 + 2*a*(p*q)) * abs(p-q) / ((p+q)**2+np.finfo('float').eps)
        return np.abs(np.sum(b))

class ChiSquareBRD(AbstractDistance):
  
    def __init__(self):
        AbstractDistance.__init__(self,"ChiSquare-BinRatioDistance")
    
    def __call__(self, p, q):
        p = np.asarray(p, dtype=np.float).flatten()
        q = np.asarray(q, dtype=np.float).flatten()
        a = np.abs(1-np.dot(p,q.T)) # NumPy needs np.dot instead of * for reducing to tensor
        b = ((p-q)**2 + 2*a*(p*q)) * (p-q)**2 / ((p+q)**3+np.finfo('float').eps)
        return np.abs(np.sum(b))
