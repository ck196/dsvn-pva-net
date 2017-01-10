from framefilejson import *
from framefilejson import jsonloader
import os
from os import path
import ujson
import sys
import argparse


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Merge model 01 and model 02')

    parser.add_argument('--input', help='prototxt file defining the network',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

args = parse_args()

with open(args.input, "r") as filereader:
    lines = filereader.readlines()
    for line in lines:
        line = line.replace("\n","")
        m1_path = line
        m2_path = line.replace("v1/","v2/")
        m3_path = line.replace("v1/","merged/")

        m1_json_obj = jsonloader.loads(m1_path)
        m2_json_obj = jsonloader.loads(m2_path)

        anno_array_01 = m1_json_obj["responses"]["annotations"]
        anno_array_02 = m2_json_obj["responses"]["annotations"]

        for ann in anno_array_02:
            if ann["object"]["detect_score"] >= 0.6:
               anno_array_01.append(ann)

        w = m2_json_obj["image_width"]
        h = m2_json_obj["image_height"]
        c = m2_json_obj["image_depth"]

        new_ann_ob = m1_json_obj
        new_ann_ob["responses"]["annotations"] = anno_array_01
        new_ann_ob["image_width"] = w
        new_ann_ob["image_height"] = h
        new_ann_ob["image_depth"] = c

        str_json = ujson.dumps(new_ann_ob)

        if not path.exists(path.dirname(m3_path)):
            try:
                os.makedirs(path.dirname(m3_path))
            except:
                pass

        with open(m3_path,"w") as filew:
            filew.write(str_json)
            filew.flush()
