import cv2
from matplotlib import pyplot as plt
import numpy as np
import sys

# Video path
import os
path = "data/SamplePOV.mp4"
print(os.path.exists(path))


if __name__ == '__main__' :

    tracker_type = 'CSRT'
    #BOOSTING, MIL, KCF, TLD, MEDIANFLOW, GOTURN, MOOSE
    tracker = cv2.legacy.TrackerCSRT_create()

    #Read Video
    vid = cv2.VideoCapture(path)

    # Exit if video not opened.
    if not vid.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = vid.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    #Create Bounding Box
    bb_x = 90
    bb_y = 23
    bb_w = 320
    bb_h = 80

    bbox = (bb_x, bb_y, bb_w, bb_h)

    while True:
        #Get new frame
        ok, frame = vid.read()
        if not ok:
            break

        #Timer
        timer = cv2.getTickCount()

        #Update Tracker
        ok, bbox = tracker.update(frame)

        #fps
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        #Draw Bounding Box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)


        cv2.imshow("Tracking", frame)


        k = cv2.waitKey(1) & 0xff
        if k == 27 : break

