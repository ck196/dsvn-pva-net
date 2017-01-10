## JSON ouput API
- A program to generate json output for [フレームファイルAPI](https://ds-teams.backlog.jp/wiki/TOYOTA_DRIVE/%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%83%95%E3%82%A1%E3%82%A4%E3%83%ABAPI)

### Requirement
- Ujson

```
pip install ujson=1.35
```

### Installing
- Clone repository
```
git clone git@bitbucket.org:datasectiondl/frame_file_json_api.git
cd frame_file_json_api
sudo python setup.py install

```

#### Import
```
from framefilejson import *

```

### Object Structure

#### Environment

```
{
    roadtype: string,
    weather: string
}

#creat object
env = Environment("ROAD_STRAIGHT", "SUNNY")
```
#### VectorOdm

```
{
    speed: float,
    turn_rate: float
}
```

#### Odometry

```
{
    direction: string,
    vectorodm: VectorOdm (working)
}

#create object
vectorodm = VectorOdm(1.73, 2.333)
odm = Odometry("FORWARD", vectorodm)

# create json_string from odm
odm_json_str = ujson.dumps(odm)

```

#### Action (working)
```
{
    motion: string,
    position: [x, y],
    radius: float,
    theta: float
}
#create object
action = Action("VERTICAL", [100, 100], 0.3, 1.3)
```

#### BoundingRect
```
{
    coordinates: array
}

#create object - We can use 2 ways. 
# coordinates = [ [x1, y1], [x2, y2]...]
coordinates = [ [0, 0], [200, 0], [0, 200], [200, 200] ]

#or

# coordinates = [ (x1, y1), (x2, y2)...]
coordinates = [ (0, 0), (200, 0), (0, 200), (200, 200) ]

rect = BoundingRect(coordinates)

```
#### Object
```
{
    id: int,
    category: MOVING|OBJECTS|ROAD_PAINTING,
    objectname: string,
    detect_score: float
}
# create object
obj = Object(-1, "PEDESTRIAN", 0.73533, category=None)
```

#### Annotation
```
{
    boundingRect: BoundingRect,
    depth: Depth,
    action: Action,
    object: Object
}

# create object
#without depth and action
annotation = Annotation(rect, obj)

# with depth and action
annotation = Annotation(rect, obj, depth, action)

```

#### AnnotationResponse
```
{
    annotations: array(Annotation)
}
#create object
annotate_response = AnnotateResponse([annotation, annotation, annotation])
```

#### Response
```
{
    frame_name: string,
    responses: AnnotationResponse,
    odometry: Odometry,
    environment: Enveronment
}
#create object
#without odometry and enviroments
responses = Responses("000001.jpg", annotate_response)

#with odometry and enviroments
responses = Responses("000001.jpg", annotate_response, odm, env)
```

### Create json from object
- We can use ujson.dumps(object) for any object.
- With Response object we can use:

```
json_string = responses.to_json(pretty=True)

# using ujson for any object
json_string = ujson.dumps(responses)


```

### Update json responses
- We have 2 methods for updating json from json string
- Method 1: Convert json string to Response object
```
import json
response = json.loads(json_string, object_hook=Response.serialize)

```
- Method2: Convert json_string to a dictionary and update directly.
```
import ujson
response_dic = ujson.loads(json_string)

#create json_string from dictionary
json_string = ujson.dumps(response_dic)

```

### Load json object from File:

```
from framefilejson import jsonloader

# load to Object
json_object = jsonloader.loads(json_file_path, object_hook=Response.serialize)

# load to dictionary
json_object = jsonloader.loads(json_file_path)

```

### Update some properties

```
from framefilejson import jsonloader

# load to Object
json_object = jsonloader.loads(json_file_path, object_hook=Response.serialize)

env = Environment("ROAD_STRAIGHT", "SUNNY")

json_object.environment = env

action = Action("ACTION")
depth = Depth(10)

annotations = json_object.get_annotations()

for annot in annotations:
    annot.update_action(action)
    annot.update_depth(depth)
    annot.update_id(3)


```

### Example

- View [demo.py](./demo.py)