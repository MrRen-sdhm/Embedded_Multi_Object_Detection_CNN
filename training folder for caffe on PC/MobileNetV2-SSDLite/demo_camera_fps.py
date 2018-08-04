# USAGE
'''
python demo_camera_fps.py --prototxt example/MobileNetV2SSDLite_deploy.prototxt \
--model models/MobileNetV2SSDLite_iter_28000.caffemodel
'''
# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

loop_cnt = 0
forward_time = 0.0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.80,
                help="minimum probability to filter weak detections")
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "5", "0", "1", "2", "3", "4"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    # vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
# otherwise, we are reading from a video file
else:
    vs = FileVideoStream(args["video"]).start()

fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()

    # frame = imutils.resize(frame, width=400)

    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    start = time.time()
    net.setInput(blob)
    detections = net.forward()

    end = time.time()
    loop_cnt += 1
    if loop_cnt > 600:
        break
    forward_time += end - start
    print forward_time, loop_cnt
    print 'Time', end - start

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                                         confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
            print label

    # show the output frame
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # completely read file so break
    if args.get("video", None) is not None:
        if vs.more() is False:
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()

print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] loop fps: {:.2f}".format(fps.fps()))
print("[INFO] forward fps: {:.2f}".format(loop_cnt / forward_time))

fo = open("fps.txt", "w")
fo.write("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
fo.write("\n")
fo.write("[INFO] loop fps: {:.2f}".format(fps.fps()))
fo.write("\n")
fo.write("[INFO] forward fps: {:.2f}".format(loop_cnt / forward_time))
fo.close()

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()