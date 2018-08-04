import numpy as np
import sys
import os
import cv2
caffe_root = '/home/sdhm/caffe/'
sys.path.insert(0, caffe_root + 'python')
import caffe


net_file = '/home/sdhm/caffe/examples/Tiny-SSD/example/TinySSD_deploy.prototxt'
caffe_model = '/home/sdhm/caffe/examples/Tiny-SSD/models/TinySSD_deploy_iter_all_30000_180317.caffemodel'
test_dir = "/home/sdhm/caffe/examples/Tiny-SSD/images/"

if not os.path.exists(caffe_model):
  print("TinySSD_deploy.caffemodel does not exist,")
  print("use merge_bn.py to generate it.")
  exit()
net = caffe.Net(net_file, caffe_model, caffe.TEST)

CLASSES = ("background", "hand", "punch", "one", "two", "three", "four")


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
  origimg = cv2.imread(imgfile)
  img = preprocess(origimg)

  img = img.astype(np.float32)
  img = img.transpose((2, 0, 1))

  net.blobs['data'].data[...] = img
  out = net.forward()
  box, conf, cls = postprocess(origimg, out)

  for i in range(len(box)):
    if conf[i] > 0.8:
      p1 = (box[i][0], box[i][1])
      p2 = (box[i][2], box[i][3])
      cv2.rectangle(origimg, p1, p2, (0, 255, 0))
      p3 = (max(p1[0], 15), max(p1[1], 15))
      title = "%s:%.2f" % (CLASSES[int(cls[i])], conf[i])
      cv2.putText(origimg, title, p3, cv2.FONT_ITALIC, 0.6, (0, 0, 255), 1)
  cv2.imshow("SSD", origimg)

  k = cv2.waitKey(0) & 0xff
  # Exit if ESC pressed
  if k == 27:
    return False
  return True


for f in os.listdir(test_dir):
  if detect(test_dir + "/" + f) == False:
    break
