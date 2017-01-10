#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Test a Fast R-CNN network on an image database."""

import _init_paths
from fast_rcnn.test import pva_detect
from fast_rcnn.config import cfg, cfg_from_file
import caffe
import time, os, sys
import cv2
import ujson


class PvaDetector():
    def __init__(self, prototxt, model_file, config_file, classes, gpu=0):

        cfg_from_file(config_file)
        cfg.GPU_ID = gpu
        caffe.set_mode_gpu()
        caffe.set_device(gpu)
        self.net = caffe.Net(prototxt, model_file, caffe.TEST)
        self.CLASSES = classes

    def detect(self, image_path, json_dir, thresh=0.1, save_img_dir=None):
        responses, img = pva_detect(self.net, image_path, thresh, self.CLASSES )
        json_file_name = "{}.json".format(responses.frame_name)
        json_file_path = os.path.join(json_dir,json_file_name)
        responses.write_to_file(json_file_path)
        return responses, img 

if __name__ == '__main__':

    CLASSES = ('__background__', # always index 0
                         'aeroplane', 'bicycle', 'bird', 'boat',
                         'bottle', 'bus', 'car', 'cat', 'chair',
                         'cow', 'diningtable', 'dog', 'horse',
                         'motorbike', 'person', 'pottedplant',
                         'sheep', 'sofa', 'train', 'tvmonitor')

    pva_detector = PvaDetector("pva-faster-rcnn/models/pvanet/full/test.pt",
                    "test.model",
                    "pva-faster-rcnn/models/pvanet/cfgs/submit_160715.yml", CLASSES)
    results, img = pva_detector.detect("test/01.jpg", "/tmp/", 0.6)

    # jsonobject = ujson.dumps(results)
    # print jsonobject

    for ann in results.responses.annotations:
        (xmin, ymin), _, (xmax, ymax), _ = ann.boundingRect.coordinates
        label = ann.object.objectname
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255,255,0), 2)
        cv2.putText(img, label, (xmin + 5, ymin + 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,255,0) , 1)

    cv2.imshow("img", img)
    cv2.waitKey(0)