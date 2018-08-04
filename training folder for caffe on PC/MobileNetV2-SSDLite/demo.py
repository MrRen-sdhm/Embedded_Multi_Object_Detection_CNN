import numpy as np
import sys
import os
import cv2
caffe_root = '/home/sdhm/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe


net_file = '/home/sdhm/caffe/examples/SqueezeNet-SSD/example/squeezenet_ssd_deploy.prototxt'
caffe_model = '/home/sdhm/caffe/examples/SqueezeNet-SSD/models/squeezenet_ssd_iter_170000.caffemodel'
test_dir = "/home/sdhm/caffe/examples/SqueezeNet-SSD/images/"

if not os.path.exists(caffe_model):
    print("SqueezeNetSSD_deploy.caffemodel does not exist,")
    print("use merge_bn.py to generate it.")
    exit()
net = caffe.Net(net_file, caffe_model, caffe.TEST)

CLASSES = ("background", "hand", "punch", "one", "two", "three", "four")
# CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
#            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
#            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
#            "sofa", "train", "tvmonitor"]


def preprocess(src):
    image = cv2.resize(src, (300, 300))
    image[:, :, 0] = (image[:, :, 0] - 104)
    image[:, :, 1] = (image[:, :, 1] - 117)
    image[:, :, 2] = (image[:, :, 2] - 123)
    return image


def postprocess(img, out):
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0, 0, :, 3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0, 0, :, 1]
    conf = out['detection_out'][0, 0, :, 2]
    return (box.astype(np.int32), conf, cls)


def detect(imgfile):
    origimg = cv2.imread(imgfile)
    img = preprocess(origimg)

    img = img.astype(np.float32)
    img = img.transpose((2, 0, 1))

    net.blobs['data'].data[...] = img
    out = net.forward()
    box, conf, cls = postprocess(origimg, out)

    for i in range(len(box)):
        if conf[i] > 0.2:
            p1 = (box[i][0], box[i][1])
            p2 = (box[i][2], box[i][3])
            cv2.rectangle(origimg, p1, p2, (0, 255, 0))
            p3 = (max(p1[0], 15), max(p1[1], 15))
            title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
            cv2.putText(origimg, title, p3, cv2.FONT_ITALIC,
                        0.6, (0, 0, 255), 1)
    cv2.imshow("SSD", origimg)

    k = cv2.waitKey(0) & 0xff
    # Exit if ESC pressed
    if k == 27:
        return False
    return True


for f in os.listdir(test_dir):
    if detect(test_dir + "/" + f) == False:
        break
