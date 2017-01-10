import json
import ujson

def loads(path, object_hook=None):
    with open(path, 'r') as f:
        if object_hook == None:
            return ujson.loads(f.read())
        else:
            return json.loads(f.read(),object_hook=object_hook)