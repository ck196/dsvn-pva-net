#!/bin/bash
set -x
set -e

LOG="train_log.txt"
exec &> >(tee -a "$LOG")
echo Logging output to "$LOG"

time ./tools/train_net.py --gpu 0 --iters 4000000 \
        --cfg models/pvanet/cfgs/train.yml \
        --imdb voc_2007_trainval \
        --solver models/pvanet/example_train_384/solver.prototxt \
        --weights models/pvanet/imagenet/original.model