import numpy as np
import sys
import os
import cv2
import caffe
from imutils import paths

caffe_root = '/home/sdhm/caffe/'
sys.path.insert(0, caffe_root + 'python')

cnt = 0

# net_file = '/home/sdhm/caffe/examples/Shufflenet-SSD/example/shufflenet_ssd_deploy.prototxt'
# caffe_model = '/home/sdhm/caffe/examples/Shufflenet-SSD/models/ShuffleNetSSD_mergebn.caffemodel'

net_file = '/home/sdhm/caffe/examples/Shufflenet-SSD/example/shufflenet_ssd_deploy_bn.prototxt'
caffe_model = '/home/sdhm/caffe/examples/Shufflenet-SSD/models/ShuffleNetSSD_iter_120000.caffemodel'

if not os.path.exists(caffe_model):
    print("ShuffleNetSSD.caffemodel does not exist,")
    print("use merge_bn.py to generate it.")
    exit()

net = caffe.Net(net_file, caffe_model, caffe.TEST)

CLASSES = ("background", " 5 ", " 0 ", " 1 ", " 2 ", " 3 ", " 4 ")
COLORS = [(255, 255, 255), (0, 255, 255), (255, 0, 255),
          (255, 255, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)]


def preprocess(src):
    img = cv2.resize(src, (300, 300))
    img = img - 127.5
    img = img * 0.007843
    return img


def postprocess(img, out):
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0, 0, :, 3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0, 0, :, 1]
    conf = out['detection_out'][0, 0, :, 2]
    return (box.astype(np.int32), conf, cls)


def detect(imgfile):
    caffe.set_device(0)
    caffe.set_mode_gpu()

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
            cv2.rectangle(origimg, p1, p2, COLORS[int(cls[i])], 2)
            y = p1[1] - 10 if p1[1] - 15 > 15 else p1[1] + 18
            title = "{}: {:.2f}%".format(CLASSES[int(cls[i])], conf[i] * 100)
            cv2.putText(origimg, title, (p1[0], y), cv2.FONT_ITALIC,
                        0.5, COLORS[int(cls[i])], 2)
            print title

    cv2.putText(origimg, 'ShuffleNetSSD', (0, origimg.shape[0] - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("ShuffleNetSSD", origimg)

    cv2.imwrite("./images_detected/" + str(cnt) +
                "-ShuffleNetSSD.jpg", origimg)

    # k = cv2.waitKey(0) & 0xff
    # # Exit if ESC pressed
    # if k == 27:
    #     return False
    # return True


imagePath = sorted(list(paths.list_images("./images1")))
for image in imagePath:
    cnt += 1
    if detect(image) == False:
        break
    print "*       *        *"
