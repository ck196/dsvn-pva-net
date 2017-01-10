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


class PvaDetector():
    def __init__(self, prototxt, model_file, config_file, classes, gpu=0):

        cfg_from_file(config_file)
        cfg.GPU_ID = gpu
        caffe.set_mode_gpu()
        caffe.set_device(gpu)
        self.net = caffe.Net(prototxt, model_file, caffe.TEST)
        self.CLASSES = classes

    def detect(self, image_path, json_dir, thresh=0.1, save_img_dir=None):
        responses = pva_detect(self.net, image_path, thresh, self.CLASSES )
        json_file_name = "{}.json".format(responses.frame_name)
        json_file_path = os.path.join(json_dir,json_file_name)
        responses.write_to_file(json_file_path)

if __name__ == '__main__':

    CLASSES = ('__background__', 'CAR', 'PEDESTRIAN', 'CYCLIST', 'HEAVY_VEHICLE', 'MOTORBIKE')

    pva_detector = PvaDetector("rcnn/pva-faster-rcnn/models/model01_deploy.prototxt",
                    "rcnn/pva-faster-rcnn/models/binary/pvanet_frcnn_384_iter_130000.caffemodel",
                    "rcnn/pva-faster-rcnn/models/pvanet/cfgs/submit_160715.yml", CLASSES)
    pva_detector.detect("rcnn/test/01.jpg", "/tmp/", 0.6)
