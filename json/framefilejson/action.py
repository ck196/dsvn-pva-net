
class Action(object):
    def __init__(self, motion=None, position=None, theta=None, radius=None):
        if motion != None:
            self._motion = motion
        if position != None:
            self._position = position
        if theta != None:
            self._theta = theta
        if radius != None:
            self._radius = radius

    @property
    def motion(self):
        return self._motion

    @motion.setter
    def motion(self, value):
        if value == None:
            raise Exception("motion cannot be empty")
        self._motion = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if value == None:
            raise Exception("position cannot be empty")
        self._position = value

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        if value == None:
            raise Exception("theta cannot be empty")
        self._theta = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value == None:
            raise Exception("action cannot be empty")
        self._radius = value

    @staticmethod
    def serialize(dic):
        motion = None
        position = None
        theta = None
        radius = None
        if 'motion' in dic:
            motion = dic['motion']
        if 'position' in dic:
            position = dic['position']
        if 'theta' in dic:
            theta = dic['theta']
        if 'radius' in dic:
            radius = dic['radius']
        return Action(motion, position, theta, radius)