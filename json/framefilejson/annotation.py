import json
import ujson
from action import Action

OJBECTS = ("PEDESTRIAN", "CYCLIST", "CAR", "BUS", "TRUCK", "HEAVY_VEHICLE",
           "MOTORBIKE", "TRAFFIC_SIGN", "GUARDRAIL", "STOPLINE", "TRAFFIC_LIGHT",
           "ONEWAY_SIGN", "NO_OVERTAKING_SIGN", "RAILROAD_CROSSING", "PEDESTRIAN_CROSSING_ZONE",
           "BICYCLE_CROSSING_ZONE", "FULLSPEED_SIGN", "CURB"
            )

class Annotation(object):
    def __init__(self, boundingRect, obj, depth = None, action = None):
        if not (boundingRect and obj) :
            raise Exception("bounding box and objectname cannot be empty")

        self._boundingRect = boundingRect
        self._object = obj

        if depth:
            self._depth = depth
        if action:
            self._action = action
        
    @property
    def boundingRect(self):
        return self._boundingRect

    @property
    def depth(self):
        return self._depth

    @property
    def action(self):
        return self._action
    
    @property
    def object(self):
        return self._object

    @boundingRect.setter
    def boundingRect(self, value):
        if not value:
            raise Exception("value cannot be empty")
        self._boundingRect = value
    
    @depth.setter
    def depth(self, value):
        if not value:
            raise Exception("value cannot be empty")
        self._depth = value

    @action.setter
    def action(self, value):
        if not value:
            raise Exception("value cannot be empty")
        self._action = value

    @object.setter
    def object(self, value):
        if not value:
            raise Exception("value cannot be empty")
        self._object = value

    @staticmethod
    def serialize(dic):
        if 'boundingRect' in dic and 'object' in dic:
            boundingRect = BoundingRect.serialize(dic['boundingRect'])
            obj = Object.serialize(dic['object'])
            depth = None
            action = None
            if 'depth' in dic and dic['depth'] != None:
                depth = Depth.serialize(dic['depth'])
            if 'action' in dic and dic['action'] != None:
                action = Action.serialize(dic['action'])

            return Annotation(boundingRect, obj, depth, action)
        else:
            return dic

    def update_depth(self, depth):
        self._depth = depth

    def update_id(self, idx):
        self._id = idx

    def update_action(self, action):
        self._action = action

    def update_object(self, object):
        self_object = object

    def update_boundingRect(self, rect):
        self._boundingRect = rect
    

class Object(object):
    def __init__(self, idx=-1, objectname=None, score=None, category=None):
        # if objectname and (objectname not in OJBECTS):
        #     raise Exception("objectname cannot be empty or not in [PEDESTRIAN, CYCLIST, CAR...]")
        self._id = idx
        if category != None:
            self._category = category
        if objectname != None:
            self._objectname = objectname
        if score != None:
            self._detect_score = score

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value == None:
            raise Exception("id cannot be empty")
        self._id = value

    @property
    def detect_score(self):
        return self._detect_score

    @detect_score.setter
    def detect_score(self, value):
        if value == None:
            raise Exception("detect_score cannot be empty")
        self._detect_score = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value == None:
            raise Exception("category cannot be empty")
        self._category = value
 
    @property
    def objectname(self):
        return self._objectname

    @objectname.setter
    def objectname(self,value):
        if value == None :
            raise Exception("objectname cannot be empty or not in [PEDESTRIAN, CYCLIST, CAR...]")
        self._objectname = value

    @staticmethod
    def serialize(dic):
        idx = 1
        category = None
        objectname = None
        score = None
        if 'category' in dic:
            category = dic['category']
        if 'objectname' in dic:
            objectname = dic['objectname']
        if 'id' in dic:
            idx = dic['id']
        if 'detect_score' in dic:
            score = dic['detect_score']
        return Object(idx, objectname, score, category)

class Depth(object):
    def __init__(self, z=None):
        if not z:
            self._z = -1
        else:
            self._z = z

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if not value:
            raise Exception("z cannot be empty")
        self._z = value

    @staticmethod
    def serialize(dic):
        if 'z' in dic:
            return Depth(dic['z'])
        else:
            return dic
    
class BoundingRect(object):
    def __init__(self, coordinates):
        if not coordinates:
            raise Exception("coordinates cannot be empty")
        if len(coordinates) == 0:
            raise TypeError("coordinates [ [x1, y1], [x2, y2]...]")
        for coord in coordinates:
            if not (isinstance(coord, tuple) or isinstance(coord, list) or len(coord) == 2):
                raise TypeError("coordinates [ [x1, y1], [x2, y2]...]")

        self._coordinates = coordinates

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        if not value:
            raise Exception("coordinates cannot be empty")
        if len(coordinates) == 0:
            raise TypeError("coordinates [ [x1, y1], [x2, y2]...]")
        for coord in coordinates:
            if not (isinstance(coord, tuple) or isinstance(coord, list) or len(coord) == 2):
                raise TypeError("coordinates [ [x1, y1], [x2, y2]...]")
        self._coordinates = value

    @staticmethod
    def serialize(dic):
        if 'coordinates' in dic:
            return BoundingRect(dic['coordinates'])
        else:
            return dic
    