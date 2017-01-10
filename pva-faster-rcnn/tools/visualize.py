import cv2
import json
import time
import os
from os import path


COLORS = ((51, 51, 255), (255, 153, 51), (51, 255, 51), (0, 0 ,255), (0,255,255), (0,128,255), (128,0,255), (102,102,255), 
        (255,102,102), (102,255,102), (255, 51, 51),(255, 128, 0), (255, 0, 255), (128, 0, 128), (51, 0, 51), (102, 0, 102)  )

#NAMES = ("__background__",'CAR', 'PEDESTRIAN', 'CYCLIST', 'HEAVY_VEHICLE', 'MOTORBIKE')

#NAMES = ("__background__",'TRAFFIC_LIGHT', "TRAFFIC_LIGHT_GREEN", "TRAFFIC_LIGHT_RED", "TRAFFIC_LIGHT_YELLOW", 'TRAFFIC_SIGN', 'PEDESTRIAN_CROSSING_ZONE')


NAMES = ('CAR', 'PEDESTRIAN', 'CYCLIST', 'HEAVY_VEHICLE', 'MOTORBIKE', 'TRAFFIC_LIGHT', "TRAFFIC_LIGHT_GREEN", "TRAFFIC_LIGHT_RED", "TRAFFIC_LIGHT_YELLOW", 'TRAFFIC_SIGN', 'PEDESTRIAN_CROSSING_ZONE')

with open("merge.txt", "r") as file_reader:
    lines = file_reader.readlines()
    for line in lines:
        image_name = line.replace("\n", "")
        print image_name
        json_file_name = image_name.replace('.jpg', '.json')
        image = cv2.imread(image_name)

        ystart = 20
        for name in NAMES:
            if name != "__background__":
                idx = NAMES.index(name)
                cv2.putText(image, name, (5, ystart), cv2.FONT_HERSHEY_COMPLEX, 0.4, COLORS[idx] , 1)
                ystart = ystart + 15

        with open(json_file_name, 'r') as json_file:
            jsonstr = json_file.read()
            annotation = json.loads(jsonstr)
            
            for an in annotation['responses']['annotations']:
                (xmin,ymin), _ , (xmax,ymax), _ = an['boundingRect']['coordinates']
                objectname = an['object']['objectname']
                #score = an['object']['detect_score']
                idx = NAMES.index(objectname)
                #if score >= 0.0:
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLORS[idx], 2)
            #cv2.imshow("image", image)
            image_name_n = image_name.replace("images","results")

            if not path.exists(path.dirname(image_name_n)):
                try:
                    os.makedirs(path.dirname(image_name_n))
                except:
                    pass
            cv2.imwrite(image_name_n, image)
            cv2.waitKey(1)
