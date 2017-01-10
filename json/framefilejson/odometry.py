from vectorodm import VectorOdm

DIRECTION = ("FORWARD", "LEFT", "RIGHT")

class Odometry(object):
    def __init__(self, direction=None, vectorodm=None):
        if direction and direction in DIRECTION:
            self._direction = direction
        if vectorodm:
            self._vectorodm = vectorodm

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if not value or (value not in DIRECTION):
            raise Exception("direction can not empty or not in ['FORWARD','LEFT', 'RIGHT']")
        self._direction = value

    @property
    def vectorodm(self):
        return self._vectorodm

    @vectorodm.setter
    def vectorodm(self, value):
        if not value:
            raise Exception("vectorodm can not empty")
        self._vectorodm = value

    @staticmethod
    def serialize(dic):
        direction = None
        vectorodm = None
        if 'direction' in dic and dic['direction'] != None:
            direction = dic['direction']
        if 'vectorodm' in dic and dic['vectorodm'] != None:
            vectorodm = VectorOdm.serialize(dic['vectorodm'])
        return Odometry(direction, vectorodm)
