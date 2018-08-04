#!/bin/sh
latest=$(ls -t snapshot/*.caffemodel | head -n 1)
if test -z $latest; then
	exit 1
fi

latest=snapshot/MobileNetV2SSDLite_iter_16000.caffemodel

../../build/tools/caffe train -solver="solver_test.prototxt" \
--weights=$latest \
-gpu 0
