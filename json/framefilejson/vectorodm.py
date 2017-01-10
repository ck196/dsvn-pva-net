

class VectorOdm(object):
    def __init__(self, speed=None, turn_rate=None):
        if speed != None:
            self._speed = speed
        if turn_rate != None:
            self._turn_rate = turn_rate

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value == None:
            raise Exception("speed can not empty")
        self._speed = value

    @property
    def turn_rate(self):
        return self._turn_rate

    @turn_rate.setter
    def turn_rate(self, value):
        if value == None:
            raise Exception("vectorodm can not empty")
        self._turn_rate = value

    @staticmethod
    def serialize(dic):
        speed = None
        turn_rate = None
        if 'speed' in dic:
            speed = dic['speed']
        if 'turn_rate' in dic:
            turn_rate = dic['turn_rate']
        return VectorOdm(speed, turn_rate)
