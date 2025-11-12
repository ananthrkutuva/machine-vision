import cv2
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import os

# Video path
path = "data/GPSSamplePOV7.mp4"
print(os.path.exists(path))

if __name__ == '__main__':

    # Use KCF tracker for stability
    l_tracker = cv2.legacy.TrackerKCF_create()
    r_tracker = cv2.legacy.TrackerKCF_create()

    # Read Video
    vid = cv2.VideoCapture(path)
    if not vid.isOpened():
        print('Could not open video file')
        sys.exit()

    ok, frame = vid.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    # Initial bounding boxes
    l_bbox = (300, 820, 420, 150)
    r_bbox = (1200, 820, 320, 150)

    l_tracker.init(frame, l_bbox)
    r_tracker.init(frame, r_bbox)

    fps_target = 30
    delay = int(1000 / fps_target)

    t = 0
    t_list = []
    theta_list = []

    while True:
        ok, frame = vid.read()
        if not ok:
            break

        t += delay / 1000
        t_list.append(t)

        l_ok, l_bbox = l_tracker.update(frame)
        r_ok, r_bbox = r_tracker.update(frame)

        if not (l_ok and r_ok):
            cv2.putText(frame, "Tracking failure detected", (100,80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Draw bounding boxes
        buffer = 5
        if l_ok:
            lx, ly, lw, lh = map(int, l_bbox)
            cv2.rectangle(frame, (lx-buffer, ly-buffer),
                          (lx+lw+buffer, ly+lh+buffer), (255,0,0), 2)
        if r_ok:
            rx, ry, rw, rh = map(int, r_bbox)
            cv2.rectangle(frame, (rx-buffer, ry-buffer),
                          (rx+rw+buffer, ry+rh+buffer), (255,0,0), 2)

        # Use center of bounding boxes as points
        l_frame_x = int(l_bbox[0] + l_bbox[2]/2)
        l_frame_y = int(l_bbox[1] + l_bbox[3]/2)
        r_frame_x = int(r_bbox[0] + r_bbox[2]/2)
        r_frame_y = int(r_bbox[1] + r_bbox[3]/2)

        # Draw points and line between them
        cv2.circle(frame, (l_frame_x, l_frame_y), 8, (0,0,255), -1)
        cv2.circle(frame, (r_frame_x, r_frame_y), 8, (0,0,255), -1)
        cv2.line(frame, (l_frame_x, l_frame_y),
                 (r_frame_x, r_frame_y), (255,0,0), 5)

        # Calculate angle
        angle_rad = -math.atan2(r_frame_y - l_frame_y,
                                r_frame_x - l_frame_x)
        theta_list.append(angle_rad)

        cv2.imshow("Tracking", frame)
        k = cv2.waitKey(int(delay/31)) & 0xff
        if k == 27:
            break

    # Vehicle position plotting
    map_x_list = [0]
    map_y_list = [0]
    velocity = 2.5
    wheel_base = 1.237
    h = delay / 1000

    # Apply calibration
    offset = -0.037
    steer_scale = 1.06
    theta_list = [theta * steer_scale + offset for theta in theta_list]

    heading = 0.0
    for t in range(len(t_list)):
        old_x = map_x_list[-1]
        old_y = map_y_list[-1]
        d = velocity * h
        theta = theta_list[t]

        epsilon = 1e-6
        if abs(math.tan(theta)) < epsilon:
            R = float('inf')
            delta_phi = 0
        else:
            R = wheel_base / math.tan(theta)
            delta_phi = d / R

        dx_local = 0
        dy_local = d
        dx = dx_local * math.cos(heading) - dy_local * math.sin(heading)
        dy = dx_local * math.sin(heading) + dy_local * math.cos(heading)

        x = old_x + dx
        y = old_y + dy
        heading += delta_phi

        map_x_list.append(x)
        map_y_list.append(y)

    plt.plot(map_x_list, map_y_list)
    plt.scatter(map_x_list[0], map_y_list[0], c="green")
    plt.scatter(map_x_list[-1], map_y_list[-1], c="red")
    plt.xlabel("X Coordinates")
    plt.ylabel("Y Coordinates")
    plt.title("Plot of Bicycle Position")
    plt.axis('equal')
    plt.legend([f'Offset = {offset}, Scale = {steer_scale}'])
    plt.show()
    plt.pause(1)
    plt.close()
