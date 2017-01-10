#!/usr/bin/env python

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Test a Fast R-CNN network on an image database."""

import _init_paths
from fast_rcnn.test import test_net
from fast_rcnn.test import pva_detect
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
import caffe
import argparse
import pprint
import time, os, sys

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Test a Fast R-CNN network')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU id to use',
                        default=0, type=int)
    parser.add_argument('--def', dest='prototxt',
                        help='prototxt file defining the network',
                        default=None, type=str)
    parser.add_argument('--net', dest='caffemodel',
                        help='model to test',
                        default=None, type=str)
    parser.add_argument('--cfg', dest='cfg_file',
                        help='optional config file', default=None, type=str)
    parser.add_argument('--wait', dest='wait',
                        help='wait until net file exists',
                        default=True, type=bool)
    parser.add_argument('--imdb', dest='imdb_name',
                        help='dataset to test',
                        default='voc_2007_test', type=str)
    parser.add_argument('--comp', dest='comp_mode', help='competition mode',
                        action='store_true')
    parser.add_argument('--set', dest='set_cfgs',
                        help='set config keys', default=None,
                        nargs=argparse.REMAINDER)
    parser.add_argument('--vis', dest='vis', help='visualize detections',
                        action='store_true')
    parser.add_argument('--num_dets', dest='max_per_image',
                        help='max number of detections per image',
                        default=100, type=int)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    #args = parse_args()

    # print('Called with args:')
    # print(args)

    # if args.cfg_file is not None:
    #     cfg_from_file(args.cfg_file)
    # if args.set_cfgs is not None:
    #     cfg_from_list(args.set_cfgs)

    cfg_from_file("models/pvanet/cfgs/submit_160715.yml")

    cfg.GPU_ID = 0

    print('Using config:')
    pprint.pprint(cfg)

    # while not os.path.exists(args.caffemodel) and args.wait:
    #     print('Waiting for {} to exist...'.format(args.caffemodel))
    #     time.sleep(10)

    caffe.set_mode_gpu()
    caffe.set_device(0)
    net = caffe.Net("output/test.prototxt", "output/pvanet_frcnn_384_iter_130000.caffemodel_used", caffe.TEST)
    net_traffic = caffe.Net("output/test.prototxt", "output/pvanet_frcnn_384_iter_130000.caffemodel_used", caffe.TEST)
    net.name = os.path.splitext(os.path.basename("output/pvanet_frcnn_384_iter_600000.caffemodel"))[0]

    #imdb = get_imdb(args.imdb_name)    
    #imdb.competition_mode(args.comp_mode)
    # if not cfg.TEST.HAS_RPN:
    #     imdb.set_proposal_method(cfg.TEST.PROPOSAL_METHOD)

    COLORS = ((51, 51, 255), (255, 153, 51), (51, 255, 51), (255,255,0), (0,255,255), (0,128,255), (128,0,255), (102,102,255), 
        (255,102,102), (102,255,102), (255, 51, 51),(255, 128, 0), (255, 0, 255), (128, 0, 128), (51, 0, 51), (102, 0, 102)  )

    CLASSES = ('__background__',
                'CAR', 'PEDESTRIAN', 'CYCLIST', 'HEAVY_VEHICLE', 'MOTORBIKE')

    with open("super.txt", "r") as filereader:
        lines = filereader.readlines()
        for line in lines:
            #print line
            line = line.replace("\n","")
            pva_detect(net, line, 0.0, vis=False, save=True, classes=CLASSES, color=COLORS)

