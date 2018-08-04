# coding:utf8
# 功能：将一个文件夹中的图片分成n组，创建n个新文件夹，并将每组图片分别移动或复制到各个文件夹中

from imutils import paths
import numpy as np
import cv2
import random
import shutil
import os

path_name = './Back'
batch_size = 50

# 打乱文件顺序
imagePaths = sorted(list(paths.list_images(path_name)))
random.seed(42)
random.shuffle(imagePaths)

foldernumber = len(imagePaths) / batch_size
print '[INFO] will sperate ' + str(len(imagePaths)) + ' images to ' + str(foldernumber) + ' folders'

for i in range(foldernumber):
    # 创建文件夹
    try:
        os.makedirs(path_name + str(i))
    except OSError as e:
        if e.errno != 17:
            print 'Some issue while creating the directory named -'
    # 移动|复制文件
    for a in range(batch_size * i, batch_size * (i + 1)):
        #移动
        # shutil.move(imagePaths[a], path_name + str(i))
        #复制
        shutil.copy(imagePaths[a], path_name + str(i))
