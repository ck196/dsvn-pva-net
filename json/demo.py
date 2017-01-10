from framefilejson import *
import ujson
import json
from os import path
from framefilejson import jsonloader

depth = Depth(10)
obj = Object(-1, PEDESTRIAN, 0.6, category=OBJECTS)

coordinates = [ (0, 0), (200, 0), (0, 200), (200, 200) ]

rect = BoundingRect(coordinates)

motion = VERTICAL
position = (100, 100)

action = Action("", (100, 100), 0.0, 0.0)

annotation = Annotation(rect, obj, action=action)

annotate_response = AnnotateResponse([annotation, annotation, annotation])

env = Environment(ROAD_STRAIGHT, SUNNY)

vectorodm =VectorOdm(6.0, 0.0)

odm = Odometry(FORWARD, vectorodm)

frame_name = "000000"

responses = Responses(frame_name, annotate_response, odometry=odm)


#responses = responses.update_weather("SUNNY")

#print respones.to_json(pretty=True)


json_str = responses.to_json()

print json_str

# Write response json content to file
json_file_name = "results/" + frame_name + ".json"

responses.write_to_file(json_file_name)

### For other object
if not path.exists(path.dirname(json_file_name)):
    try:
        os.makedirs(path.dirname(json_file_name))
    except:
        pass

with open(json_file_name, "w") as file_writer:
    file_writer.write(ujson.dumps(responses))

# Method 1

json_obj = jsonloader.loads("results/000000.json", object_hook=Responses.serialize)

print json_obj.odometry.vectorodm.turn_rate

#print json_obj.environment.weather

#json_obj = json_obj.update_roadtype("STRAIGHT")

json_obj.write_to_file("results/000001.json")

# for annot in json_obj.get_annotations():
#     annot.update_depth(depth)
#     annot.update_action(action)
#     annot.update_id(3)

# #json_obj.update_depth(0,depth)

# print ujson.dumps(json_obj)

# #Method 2 : Using dictionary

# json_dic = jsonloader.loads(json_file_name)

# # print json_dic['environment']
# # print json_dic['odometry']

# print json_dic['responses']['annotations'][0]['object']
# print json_dic['responses']['annotations'][0]['boundingRect']
# print json_dic['responses']['annotations'][0]['action']
