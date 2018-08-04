#!/bin/bash

# 生成折线图和两个文件:
./plot_training_log.py.example 0 caffe.sdhm-X450JF.sdhm-0.log

# Usage:
#     ./plot_training_log.py chart_type[0-7] /path/to/first.log ...
# Notes:
#     1. Supporting multiple logs.
#     2. Log file name must end with the lower-cased ".log".
# Supported chart types:
#     0: Test accuracy  vs. Iters
#     1: Test accuracy  vs. Seconds
#     2: Test loss  vs. Iters
#     3: Test loss  vs. Seconds
#     4: Train learning rate  vs. Iters
#     5: Train learning rate  vs. Seconds
#     6: Train loss  vs. Iters
#     7: Train loss  vs. Seconds

