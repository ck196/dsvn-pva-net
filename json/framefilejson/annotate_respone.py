from annotation import Annotation

class AnnotateResponse(object):
    def __init__(self, annotations=None):
        if annotations:
            self._annotations = annotations
        else:
            self._annotations = []

    @property
    def annotations(self):
        return self._annotations
    
    @annotations.setter
    def annotations(self, value):
        self._annotations = value

    @staticmethod
    def serialize(dic):
        if 'annotations' in dic:
            annotations = []
            for ann in dic['annotations']:
                annotations.append(Annotation.serialize(ann))
            return AnnotateResponse(annotations)
        else:
            return dic