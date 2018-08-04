#!/bin/sh
if ! test -f example/TinySSD_train.prototxt ;then
	echo "error: example/TinySSD_train.prototxt does not exist."
	echo "please use the gen_model.sh to generate your own model."
        exit 1
fi
mkdir -p snapshot

## train based on weight
# GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
# ../../build/tools/caffe train -solver="solver_train.prototxt" \
# # -weights="./weight/TinySSD_iter_153000.caffemodel" \
# -gpu 0

## train based on solverstate
GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
../../build/tools/caffe train -solver="solver_train.prototxt" \
-snapshot=./snapshot/TinySSD_iter_163389.solverstate \
-gpu 0
