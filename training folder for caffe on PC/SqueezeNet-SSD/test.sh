#!/bin/sh
latest=$(ls -t snapshot/*.caffemodel | head -n 1)
if test -z $latest; then
	exit 1
fi

latest=models/squeezenet_ssd_iter_170000.caffemodel

../../build/tools/caffe train -solver="solver_test.prototxt" \
--weights=$latest \
-gpu 0
