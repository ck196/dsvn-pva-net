

TYPE = ("ROAD_STRAIGHT", "ROAD_INTERSECTION")
WEATHER = ("SUNNY", "CLOUDY", "RAINY")
LIGHT = ("DAY", "NIGHT")

class Environment(object):
    def __init__(self, roadtype=None, weather=None, light=None):
        if roadtype != None:
            self._roadtype = roadtype
        if weather != None:
            self._weather = weather
        if light != None:
            self._light = light

    @property
    def roadtype(self):
        return self._roadtype

    @roadtype.setter
    def roadtype(self, value):
        if not value or (value not in TYPE):
            raise Exception("roadtype cannot be empty or not in [ROAD_STRAIGHT, ROAD_INTERSECTION]")
        self._roadtype = value

    @property
    def weather(self):
        return self._weather

    @weather.setter
    def weather(self, value):
        if not value or (value not in WEATHER):
            raise Exception("weather cannot be empty or not in [SUNNY, RAINY, CLOUDY]")
        self._weather = value


    @property
    def light(self):
        return self._light

    @light.setter
    def light(self, value):
        if not value or (value not in LIGHT):
            raise Exception("roadtype cannot be empty or not in [ROAD_STRAIGHT, ROAD_INTERSECTION]")
        self._light = value


    @staticmethod
    def serialize(dic):
        roadtype = None
        weather = None
        light = None

        if 'roadtype' in dic:
            roadtype = dic['roadtype']
        if 'weather' in dic:
            weather = dic['weather']
        if 'light' in dic:
            light = dic['light']

        return Environment(roadtype,weather,light)
    