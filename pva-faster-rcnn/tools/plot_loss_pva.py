#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 Takuma Yagi <takuma.yagi@datasection.co.jp>
#
# Distributed under terms of the MIT license.

import sys, os
import re
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":


    argv = sys.argv

    if len(argv) != 3:
        print "Usage: python plot_loss.py <log_file_path> <conv_r>"
        quit()

    # プロットの平滑化パラメタ
    # conv_r個の移動平均を取る
    conv_r = float(argv[2])

    

    train_loss = []
    train_acc = []
    test_loss = []
    test_acc = []

    loss_bbox = []
    loss_cls = []
    rpn_cls_loss = []
    rpn_loss_bbox = []

    f = open(argv[1])
    outfile = "loss_plot_%s.png" % os.path.splitext(os.path.basename(argv[1]))[0]
    lines = f.readlines()

    for index in range(0,len(lines)):
        line = lines[index].strip()
        if "Iteration" in line and "loss =" in line:
            #print lines[index]
            try:
                step = int(re.search('Iteration ([0-9]+)', line).groups()[0])
                tr_l = float(re.search('loss = ([0-9\.]+)', line).groups()[0])
                train_loss.append([step, tr_l])
                line = lines[index + 1].strip()
                tr_l = float(re.search('cls_loss = ([0-9\.]+)', line).groups()[0])
                loss_bbox.append([step, tr_l])
                line = lines[index + 2].strip()
                tr_l = float(re.search('loss_bbox = ([0-9\.]+)', line).groups()[0])
                loss_cls.append([step, tr_l])
                line = lines[index + 3].strip()
                tr_l = float(re.search('rpn_cls_loss = ([0-9\.]+)', line).groups()[0])
                rpn_cls_loss.append([step, tr_l])
                line = lines[index + 4].strip()
                tr_l = float(re.search('rpn_loss_bbox = ([0-9\.]+)', line).groups()[0])
                rpn_loss_bbox.append([step, tr_l])
            except:
                pass

        # line = f.readline().strip()

    train_loss = np.asarray(train_loss)
    train_loss_ave = np.convolve(train_loss[:,1], np.ones(int(conv_r))/conv_r, 'same')

    loss_bbox = np.asarray(loss_bbox)
    loss_bbox_ave = np.convolve(loss_bbox[:,1], np.ones(int(conv_r))/conv_r, 'same')

    loss_cls = np.asarray(loss_cls)
    loss_cls_ave = np.convolve(loss_cls[:,1], np.ones(int(conv_r))/conv_r, 'same')

    rpn_cls_loss = np.asarray(rpn_cls_loss)
    rpn_cls_loss_ave = np.convolve(rpn_cls_loss[:,1], np.ones(int(conv_r))/conv_r, 'same')

    rpn_loss_bbox = np.asarray(rpn_loss_bbox)
    rpn_loss_bbox_ave = np.convolve(rpn_loss_bbox[:,1], np.ones(int(conv_r))/conv_r, 'same')

    if not len(train_loss) > 2:
        quit()

    fig, ax1 = plt.subplots(figsize=(12,9))
    ax1.set_xlim([1, max(train_loss[:, 0])])
    ax1.set_ylim([0.0, 5.0])
    ax1.set_xlabel('step')
    ax1.set_ylabel('loss')
    ax1.plot(train_loss[:, 0], train_loss_ave,
                label='training loss', c='b')
    ax1.plot(loss_bbox[:, 0], loss_bbox_ave,
                label='loss_bbox', c='g')
    ax1.plot(loss_cls[:, 0], loss_cls_ave,
                label='loss_cls', c='r')
    ax1.plot(rpn_cls_loss[:, 0], rpn_cls_loss_ave,
                label='rpn_cls_loss', c='y')
    ax1.plot(rpn_loss_bbox[:, 0], rpn_loss_bbox_ave,
                label='rpn_loss_bbox', c='m')
    ax1.axhline(y=0.2, color="black", ls="dotted")
    ax1.axhline(y=0.25, color="black", ls="dotted")
    """
    ax1.plot(train_loss[:, 0], train_loss[:, 1],
                label='training loss', c='b')
    ax1.plot(train_loss[:, 0], train_loss[:, 1],
                label='training loss', c='b')
    """
    #ax1.plot(test_loss[:, 0], test_loss[:, 1],
    #            label='test loss', c='g')

    #ax2 = ax1.twinx()
    """
    ax2.plot(test_acc[:, 0], test_acc[:, 1], label='test accuracy', c='c')
    ax2.plot(validation_acc[:, 0], validation_acc[:, 1], label='validation accuracy', c='m')
    ax2.set_xlim([1, max(train_loss[:, 0])])
    ax2.set_ylabel('accuracy')
    """

    ax1.legend(bbox_to_anchor=(0.25, -0.1), loc=9)
    #ax2.legend(bbox_to_anchor=(0.75, -0.1), loc=9)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.title("loss of faster R-CNN: convolve=%d\n%s" % (int(conv_r), os.path.basename(argv[1])))
    plt.savefig(outfile, bbox_inches='tight')
    print "Figure saved: %s" % outfile
    plt.pause(30)
    plt.close()

    f.close()
