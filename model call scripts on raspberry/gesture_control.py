# USAGE
# python gesture_control.py --graph graphs/GestureRecognize_6types_iter156000_graph --display 1

# import the necessary packages
from mvnc import mvncapi as mvnc
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import numpy as np
import time
import cv2

realtime_fps = 0
temperature = 20
lampstate = 'OFF'
is_cnt = 0
click = 0

# initialize the list of class labels our network was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ("background", " 5 ", " 0 ", " 1 ", " 2 ", " 3 ", " 4 ")
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


def preprocess_image(input_image):
    # preprocess the image
    preprocessed = cv2.resize(input_image, (300, 300))
    preprocessed = preprocessed - 127.5
    preprocessed = preprocessed * 0.007843
    preprocessed = preprocessed.astype(np.float16)

    # return the image to the calling function
    return preprocessed


def predict(image, graph):
    # preprocess the image
    image = preprocess_image(image)

    # send the image to the NCS and run a forward pass to grab the
    # network predictions
    graph.LoadTensor(image, None)
    (output, _) = graph.GetResult()

    # grab the number of valid object predictions from the output,
    # then initialize the list of predictions
    num_valid_boxes = output[0]
    predictions = []

    # loop over results
    for box_index in range(num_valid_boxes):
        # calculate the base index into our array so we can extract
        # bounding box information
        base_index = 7 + box_index * 7

        # boxes with non-finite (inf, nan, etc) numbers must be ignored
        if (not np.isfinite(output[base_index]) or
                not np.isfinite(output[base_index + 1]) or
                not np.isfinite(output[base_index + 2]) or
                not np.isfinite(output[base_index + 3]) or
                not np.isfinite(output[base_index + 4]) or
                not np.isfinite(output[base_index + 5]) or
                not np.isfinite(output[base_index + 6])):
            continue

        # extract the image width and height and clip the boxes to the
        # image size in case network returns boxes outside of the image
        # boundaries
        (h, w) = image.shape[:2]
        x1 = max(0, int(output[base_index + 3] * w))
        y1 = max(0, int(output[base_index + 4] * h))
        x2 = min(w, int(output[base_index + 5] * w))
        y2 = min(h, int(output[base_index + 6] * h))

        # grab the prediction class label, confidence (i.e., probability),
        # and bounding box (x, y)-coordinates
        pred_class = int(output[base_index + 1])
        pred_conf = output[base_index + 2]
        pred_boxpts = ((x1, y1), (x2, y2))

        # create prediciton tuple and append the prediction to the
        # predictions list
        prediction = (pred_class, pred_conf, pred_boxpts)
        predictions.append(prediction)

    # return the list of predictions to the calling function
    return predictions


def click_and_crop(event, x, y, flags, param):
    global click
    # left mouse button clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        click = 1


def gesture_control(pred_class):
    global lampstate, temperature, is_cnt
    if CLASSES[pred_class] == " 0 ":
        lampstate = 'OFF'
    elif CLASSES[pred_class] == " 5 ":
        lampstate = 'ON'
    elif CLASSES[pred_class] == " 1 " and is_cnt == 0:
        if temperature < 30:
            temperature += 1
    elif CLASSES[pred_class] == " 2 " and is_cnt == 0:
        if temperature > 16:
            temperature -= 1


        # construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--graph", required=True,
                help="path to input graph file")
ap.add_argument("-c", "--confidence", default=0.95,
                help="confidence threshold")
ap.add_argument("-d", "--display", type=int, default=0,
                help="switch to display image on screen")
ap.add_argument("-f", "--full", type=int, default=1,
                help="switch the display mode")
args = vars(ap.parse_args())

# grab a list of all NCS devices plugged in to USB
print("[INFO] finding NCS devices...")
devices = mvnc.EnumerateDevices()

# if no devices found, exit the script
if len(devices) == 0:
    print("[INFO] No devices found. Please plug in a NCS")
    quit()

# use the first device since this is a simple test script
# (you'll want to modify this is using multiple NCS devices)
print("[INFO] found {} devices. device0 will be used. "
      "opening device0...".format(len(devices)))
device = mvnc.Device(devices[0])
device.OpenDevice()

# open the CNN graph file
print("[INFO] loading the graph file into RPi memory...")
with open(args["graph"], mode="rb") as f:
    graph_in_memory = f.read()

# load the graph into the NCS
print("[INFO] allocating the graph on the NCS...")
graph = device.AllocateGraph(graph_in_memory)

# create a full screen window
cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Output", click_and_crop)
if args["full"]:
    cv2.setWindowProperty("Output", 0, 1)

# open a pointer to the video stream thread and allow the buffer to
# start to fill, then start the FPS counter
print("[INFO] starting the video stream and FPS counter...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(1)
fps = FPS().start()

# loop over frames from the video file stream
while True:
    try:
        start = time.time()

        # grab the frame from the threaded video stream
        frame = vs.read()

        # use the NCS to acquire predictions
        predictions = predict(frame, graph)

        # loop over our predictions
        for (i, pred) in enumerate(predictions):
            # extract prediction data for readability
            (pred_class, pred_conf, pred_boxpts) = pred

            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if pred_conf > args["confidence"]:
                # control device by gestures
                gesture_control(pred_class)

                # record the number of times the gesture was detected
                is_cnt += 1
                if is_cnt > 3:
                    is_cnt = 0

                # # print prediction to terminal
                # print("[INFO] Prediction #{}: class={}, confidence={}, "
                #       "boxpoints={}".format(i, CLASSES[pred_class], pred_conf,
                #                             pred_boxpts))

                # check if we should show the prediction data
                # on the frame
                if args["display"] > 0:
                    # build a label consisting of the predicted class and
                    # associated probability
                    label = "{}: {:.2f}%".format(CLASSES[pred_class],
                                                 pred_conf * 100)

                    # extract information from the prediction boxpoints
                    (ptA, ptB) = (pred_boxpts[0], pred_boxpts[1])
                    (startX, startY) = (ptA[0], ptA[1])
                    y = startY - 5 if startY - 15 > 15 else startY + 15

                    # display the rectangle and label text
                    cv2.rectangle(frame, ptA, ptB,
                                  COLORS[pred_class], 2)
                    cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[pred_class], 2)
            else:
                if is_cnt > 0:
                    is_cnt -= 1

            # print is_cnt

        # check if we should display the frame on the screen
        # with prediction data (you can achieve faster FPS if you
        # do not output to the screen)
        if args["display"] > 0:
            # display the frame to the screen
            frame = cv2.resize(frame, (0, 0), fx=1.125, fy=1,
                               interpolation=cv2.INTER_NEAREST)
            cv2.rectangle(frame, (0, int(frame.shape[0] * 0.92)),
                          (frame.shape[1], frame.shape[0]), (255, 255, 255), -1)
            label = "{}: {:.1f}".format("fps", realtime_fps)
            cv2.putText(frame, label, (5, int(frame.shape[0] * 0.972)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(frame, "temperature: ", (80, int(frame.shape[0] * 0.972)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(frame, str(temperature), (195, int(frame.shape[0] * 0.972)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(frame, "lampstate: ", (230, int(frame.shape[0] * 0.972)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(frame, lampstate, (320, int(frame.shape[0] * 0.972)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow("Output", frame)

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
            if click == 1:
                break

        # update the FPS counter
        fps.update()

        end = time.time()
        realtime_fps = 1 / (end - start)

    # if "ctrl+c" is pressed in the terminal, break from the loop
    except KeyboardInterrupt:
        break

    # if there's a problem reading a frame, break gracefully
    except AttributeError:
        break

# stop the FPS counter timer
fps.stop()

# destroy all windows if we are displaying them
if args["display"] > 0:
    cv2.destroyAllWindows()

# stop the video stream
vs.stop()

# clean up the graph and device
graph.DeallocateGraph()
device.CloseDevice()

# display FPS information
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
