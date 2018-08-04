#!/bin/sh
if ! test -f example/MobileNetV2SSDLite_train.prototxt ;then
	echo "error: example/MobileNetV2SSDLite_train.prototxt does not exist."
	echo "please use the gen_model.sh to generate your own model."
        exit 1
fi
mkdir -p snapshot

## train based on weight
# GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
# ../../build/tools/caffe train -solver="solver_train.prototxt" \
# -weights="./weight/MobileNetV2SSDLite_iter_28000.caffemodel" \
# -gpu 0

## train based on solverstate
GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
../../build/tools/caffe train -solver="solver_train.prototxt" \
-snapshot=./snapshot/MobileNetV2SSDLite_iter_18619.solverstate \
-gpu 0
