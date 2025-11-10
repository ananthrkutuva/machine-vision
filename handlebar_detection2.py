import cv2
from matplotlib import pyplot as plt
import numpy as np
import sys
import math
import matplotlib.pyplot as plt

# Video path
import os
path = "data/SamplePOV5.mp4"
print(os.path.exists(path))


if __name__ == '__main__' :

    tracker_type = 'CSRT'
    #BOOSTING, MIL, KCF, TLD, MEDIANFLOW, GOTURN, MOOSE
    l_tracker = cv2.legacy.TrackerCSRT_create()
    r_tracker = cv2.legacy.TrackerCSRT_create()


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

    #Create Bounding Boxes
    l_bb_x = 350
    l_bb_y = 600
    l_bb_w = 450
    l_bb_h = 230

    r_bb_x = 1150
    r_bb_y = 650
    r_bb_w = 400
    r_bb_h = 230
   

    l_bbox = (l_bb_x, l_bb_y, l_bb_w, l_bb_h)
    r_bbox = (r_bb_x, r_bb_y, r_bb_w, r_bb_h)



    # Desired playback fps
    fps_target = 30

    # Compute wait time per frame in ms
    video_fps = vid.get(cv2.CAP_PROP_FPS)
    comp_delay = int(1000 / video_fps)

    delay = int(1000 / fps_target)


    #Initialize Tracker
    l_tracker.init(frame, l_bbox)
    r_tracker.init(frame, r_bbox)

    #maths for plotting
    t = 0
    t_list = []
    theta_list = []

    while True:
        #Get new frame
        ok, frame = vid.read()
        if not ok:
            break
        
        #Timer
        timer = cv2.getTickCount()
        t+=delay/1000
        t_list.append(t)

        #Update Tracker
        l_ok, l_bbox = l_tracker.update(frame)
        r_ok, r_bbox = r_tracker.update(frame)

        #fps
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        buffer = 5

        #Draw Bounding Box
        if l_ok & r_ok:
            p1 = (int(l_bbox[0] - buffer), int(l_bbox[1] - buffer)) #make sure bbox isnt in ROI frame
            p2 = (int(l_bbox[0] + l_bbox[2] + buffer), int(l_bbox[1] + l_bbox[3] + buffer))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            p1 = (int(r_bbox[0] - buffer), int(r_bbox[1] - buffer)) #make sure bbox isnt in ROI frame
            p2 = (int(r_bbox[0] + r_bbox[2] + buffer), int(r_bbox[1] + r_bbox[3] + buffer))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)


        cv2.imshow("Tracking", frame)

        # Get frame dimensions
        frame_h, frame_w = frame.shape[:2]

        # Left ROI
        x, y, w, h = map(int, l_bbox)

        # Clamp x and y to be inside frame
        x = max(0, x)
        y = max(0, y)

        # Clamp width and height so ROI stays inside frame
        w = min(w, frame_w - x)
        h = min(h, frame_h - y)

        # Skip frame if ROI is completely invalid
        if w <= 0 or h <= 0:
            print("Left ROI out of frame, skipping")
            continue

        l_roi = frame[y:y+h, x:x+w]

        # Right ROI (same logic)
        x, y, w, h = map(int, r_bbox)
        x = max(0, x)
        y = max(0, y)
        w = min(w, frame_w - x)
        h = min(h, frame_h - y)

        if w <= 0 or h <= 0:
            print("Right ROI out of frame, skipping")
            continue

        r_roi = frame[y:y+h, x:x+w]

        #Convert to greyscale
        l_grey = cv2.cvtColor(l_roi, cv2.COLOR_BGR2GRAY)
        r_grey = cv2.cvtColor(r_roi, cv2.COLOR_BGR2GRAY)

        #Show
        cv2.imshow("L Greyscale ROI", l_grey)
        cv2.imshow("R Greyscale ROI", r_grey)

        l_edges = cv2.Canny(l_grey, 150, 300, apertureSize=3)
        r_edges = cv2.Canny(r_grey, 150, 300, apertureSize=3)
        cv2.imshow("L Edges ROI", l_edges)
        cv2.imshow("R Edges ROI", r_edges)

        l_lines = cv2.HoughLinesP(l_edges, 1, np.pi/180, threshold=32, minLineLength=30, maxLineGap=15)
        r_lines = cv2.HoughLinesP(r_edges, 1, np.pi/180, threshold=32, minLineLength=30, maxLineGap=15)

        b_thresh = 50

        if l_lines is not None:
            for line in l_lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(l_roi, (x1,y1), (x2, y2), (0,255,0), 2) #from testing x2 is always bigger than x1 :)

        if r_lines is not None:
            for line in r_lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(r_roi, (x1,y1), (x2, y2), (0,255,0), 2) #from testing x2 is always bigger than x1 :)

        l_lines = [l[0] for l in l_lines]
        r_lines = [l[0] for l in r_lines]
        l_mid_x_list = []
        l_mid_y_list = []
        r_mid_x_list = []
        r_mid_y_list = []

        for (x1, y1, x2, y2) in l_lines:
            l_mid_x_list.append((x1 + x2) / 2)
            l_mid_y_list.append((y1 + y2) / 2)

        for (x1, y1, x2, y2) in r_lines:
            r_mid_x_list.append((x1 + x2) / 2)
            r_mid_y_list.append((y1 + y2) / 2)

        l_avg_mid_x = int(sum(l_mid_x_list) / len(l_mid_x_list))
        l_avg_mid_y = int(sum(l_mid_y_list) / len(l_mid_y_list))
        r_avg_mid_x = int(sum(r_mid_x_list) / len(r_mid_x_list))
        r_avg_mid_y = int(sum(r_mid_y_list) / len(r_mid_y_list))


        l_roi_x = 250  # constant inside left ROI
        l_roi_y = l_avg_mid_y  # y from average of Hough lines
        # Convert to frame coordinates
        l_frame_x = int(l_bbox[0] + l_roi_x)
        l_frame_y = int(l_bbox[1] + l_roi_y)

        # Draw in full frame
        cv2.circle(frame, (l_frame_x, l_frame_y), 8, (0, 0, 255), -1)

        r_roi_x = 200  # constant inside right ROI
        r_roi_y = r_avg_mid_y  # y from average of Hough lines

        # Convert to frame coordinates
        r_frame_x = int(r_bbox[0] + r_roi_x)
        r_frame_y = int(r_bbox[1] + r_roi_y)

        # Draw in full frame
        cv2.circle(frame, (r_frame_x, r_frame_y), 8, (0, 0, 255), -1)
          # red filled
        cv2.line(frame, (l_frame_x, l_frame_y), (r_frame_x, r_frame_y), (255,0,0), 5)

        cv2.imshow("L ROI", l_roi)
        cv2.imshow("R ROI", r_roi)
        cv2.imshow("Tracking", frame)

        #Go through the lines and calc line for tracking
        angle_rad = math.atan2(r_frame_y-l_frame_y, r_frame_x-l_frame_x) # angle in radians
        theta_list.append(angle_rad)

        

        k = cv2.waitKey(delay) & 0xff
        if k == 27 : break

        

    print(theta_list)
    print(t_list)
    print(len(theta_list))
    print(len(t_list))

    map_x_list = [0]
    map_y_list = [0]

    velocity = 3 #m/s constant change later
    wheel_base = 1.237 #meters
    h = delay/1000 #timestep in s

    #Tune Theta list by callibrated value
    offset = -0.05 # add 0.05 rad to all values

    theta_list = [theta + offset for theta in theta_list]


    for t in range(len(t_list)):
        old_x = map_x_list[-1]
        old_y = map_y_list[-1]
        print(t)
        d = velocity * h
        R = wheel_base / math.tan(theta_list[t])
        delta_phi = d / R 

        dx = R * (1 - math.cos(delta_phi))
        dy = R * math.sin(delta_phi)

        x = old_x + dx
        y = old_y + dy

        map_x_list.append(x)
        map_y_list.append(y)

    print(map_x_list)
    print(map_y_list)
    print(len(map_y_list))

    init_x = map_x_list[0]
    init_y = map_y_list[0]
    final_x = map_x_list[-1]
    final_y = map_y_list[-1]

    plt.plot(map_x_list, map_y_list)
    plt.scatter(init_x, init_y, c="green")
    plt.scatter(final_x, final_y, c="red")
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Plot of Bicycle Position")
    # plt.axis('equal')
    plt.show()
    plt.pause(1)
    plt.close()

