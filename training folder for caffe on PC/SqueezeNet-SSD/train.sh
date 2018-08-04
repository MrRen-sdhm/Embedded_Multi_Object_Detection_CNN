#!/bin/sh
if ! test -f example/squeezenet_ssd_train.prototxt ;then
	echo "error: example/squeezenet_ssd_train.prototxt does not exist."
	echo "please use the gen_model.sh to generate your own model."
        exit 1
fi
mkdir -p snapshot

## train based on weight
GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
../../build/tools/caffe train -solver="solver_train.prototxt" \
-weights="./weight/squeezenet_ssd_iter_50000.caffemodel" \
-gpu 0

# train based on solverstate
GLOG_logtostderr=0 GLOG_log_dir=./log/logfile \
../../build/tools/caffe train -solver="solver_train.prototxt" \
-snapshot=./snapshot/squeezenet_ssd_iter_75354.solverstate \
-gpu 0
