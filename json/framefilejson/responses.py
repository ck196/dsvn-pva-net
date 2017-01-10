import ujson
import json
from environment import Environment
from odometry import Odometry
from annotate_respone import AnnotateResponse

class Responses(object):
    def __init__(self, frame_name, responses, width=None, height=None, depth=None, odometry=None, environment=None):
        if not (responses and frame_name):
            raise Exception("properties cannot be empty")
        self._frame_name = frame_name
        self._responses = responses
        if odometry:
            self._odometry = odometry
        if environment:
            self._environment = environment
        if width:
            self._image_width = width
        if height:
            self._image_height = height
        if depth:
            self._image_depth = depth


    @property
    def frame_name(self):
        return self._frame_name

    @property
    def responses(self):
        return self._responses

    @property
    def odometry(self):
        return self._odometry
    
    @property
    def environment(self):
        return self._environment
    
    @responses.setter
    def responses(self, value):
        if not value:
            raise Exception("responses cannot be empty")
        self._responses = value

    @odometry.setter
    def odometry(self, value):
        if not value:
            raise Exception("odometry cannot be empty")
        self._odometry = value

    @environment.setter
    def environment(self, value):
        if not value:
            raise Exception("environment cannot be empty")
        self._environment = value

    @frame_name.setter
    def frame_name(self, value):
        if not value:
            raise Exception("framename cannot be empty")
        self._frame_name = value


    @property
    def image_width(self):
        return self._image_width

    @property
    def image_height(self):
        return self._image_height

    @property
    def image_depth(self):
        return self._image_depth

    @image_width.setter
    def image_width(self, value):
        if not value:
            raise Exception("responses cannot be empty")
        self._image_width = value

    @image_height.setter
    def image_height(self, value):
        if not value:
            raise Exception("responses cannot be empty")
        self._image_height = value

    @image_depth.setter
    def image_depth(self, value):
        if not value:
            raise Exception("responses cannot be empty")
        self._image_depth = value

    def to_json(self, pretty=False):
        if pretty:
            return ujson.dumps(self, indent=4)
        return ujson.dumps(self)

    def update_depth(self, index, depth):
        self.responses.annotations[index].depth = depth

    def update_action(self, index, action):
        self.responses.annotations[index].action = action

    def update_id(self, index, idx):
        self.responses.annotations[index].object.id = idx

    def write_to_file(self, out_path):
        with open(out_path, 'w') as file_writer:
            file_writer.write(ujson.dumps(self))

    def get_annotations(self):
        return self.responses.annotations

    def update_weather(self, weather):
        env = None
        action = None
        odm = None
        w = None
        h = None
        c = None

        if hasattr(self,'_environment'):
            env = self.environment
        if hasattr(self,'_odometry'):
            odm = self.odometry
        if hasattr(self,'_action'):
            action = self.action

        if hasattr(self,'_image_depth'):
            c = self.image_depth
        if hasattr(self,'_image_height'):
            h = self.image_height
        if hasattr(self,'_image_width'):
            w = self.image_width

        if not hasattr(self, '_enviroment'):
            env = Environment(weather = weather)
            self = Responses(self.frame_name, self.responses, width=w, height=h, depth=c, odometry=odm, environment=env)
        else:
            light = None,
            roadtype = None

            if hasattr(self.environment, '_light'):
                light = self.environment.light

            if hasattr(self.environment, '_roadtype'):
                roadtype = self.environment.roadtype

            self.environment = Environment(roadtype, weather, light)

        return self

    def update_light(self, light):
        env = None
        action = None
        odm = None
        w = None
        h = None
        c = None

        if hasattr(self,'_environment'):
            env = self.environment
        if hasattr(self,'_odometry'):
            odm = self.odometry
        if hasattr(self,'_action'):
            action = self.action

        if hasattr(self,'_image_depth'):
            c = self.image_depth
        if hasattr(self,'_image_height'):
            h = self.image_height
        if hasattr(self,'_image_width'):
            w = self.image_width

        if not hasattr(self, '_environment'):
            env = Environment(light = light)
            self = Responses(self.frame_name, self.responses, width=w, height=h, depth=c, odometry=odm, environment=env)
        else:
            roadtype = None
            weather = None

            if hasattr(self.environment, '_weather'):
                weather = self.environment.weather

            if hasattr(self.environment, '_roadtype'):
                roadtype = self.environment.roadtype

            self.environment = Environment(roadtype, weather, light)

        return self


    def update_roadtype(self, roadtype):
        env = None
        action = None
        odm = None
        w = None
        h = None
        c = None

        if hasattr(self,'_environment'):
            env = self.environment
        if hasattr(self,'_odometry'):
            odm = self.odometry
        if hasattr(self,'_action'):
            action = self.action

        if hasattr(self,'_image_depth'):
            c = self.image_depth
        if hasattr(self,'_image_height'):
            h = self.image_height
        if hasattr(self,'_image_width'):
            w = self.image_width

        if not hasattr(self, '_environment'):
            env = Environment(roadtype = roadtype)
            self = Responses(self.frame_name, self.responses, width=w, height=h, depth=c, odometry=odm, environment=env)
        else:
            light = None
            _roadtype = None
            weather = None

            if hasattr(self.environment, '_weather'):
                weather = self.environment.weather

            if hasattr(self.environment, '_light'):
                light = self.environment.light

            self.environment = Environment(roadtype, weather, light)

        return self


    @staticmethod
    def serialize(dic):
        if 'responses' in dic  and 'frame_name' in dic:
            responses = AnnotateResponse.serialize(dic['responses'])
            env = None
            odometry = None
            width = None
            height = None
            depth = None
            if 'odometry' in dic and dic['odometry'] != None:
                odometry = Odometry.serialize(dic['odometry'])
            if 'environment' in dic and dic['environment'] != None:
                env = Environment.serialize(dic['environment'])
            if 'image_width' in dic:
                width = dic['image_width']
            if 'image_height' in dic:
                height = dic['image_height']
            if 'image_depth' in dic:
                depth = dic['image_depth']
            return Responses(dic['frame_name'], responses, width, height, depth, odometry, env)
        else:
            return dic