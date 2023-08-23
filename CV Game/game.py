
import cv2
import numpy as np
import random
import time
from ultralytics import YOLO
model = YOLO('/Users/madhuupadhyay/Documents/Whack-a-crypto/runs/detect/train7/weights/best.pt')

# Open the webcam
cap = cv2.VideoCapture(1)

# Resize the static image to a smaller size
desired_static_width = 100  # You can adjust this value
last_coordinates_change_time = time.time()
key = 0
x_offset = 0
y_offset = 0
timer = 0
start = time.time()
score = 0
xmin = 0
ymin = 0
xmax = 0
ymax = 0
el=0

while timer<30:
    ret, frame = cap.read()

    if not ret:
        break
    
    # Calculate elapsed time since last coordinate change
    elapsed_time = time.time() - last_coordinates_change_time
    
    # If 1 second has elapsed, change the coordinates and key value
    if elapsed_time >= 1.0:
        x_offset = random.randint(0, frame.shape[1] - desired_static_width)
        y_offset = random.randint(0, frame.shape[0] - desired_static_height)
        key = random.randint(0, 2)  # Generate a random value between 0 and 2
        last_coordinates_change_time = time.time()

    
    # Load the static image based on the key value
    if key == 0:
        static_image = cv2.imread('CV Game/Assets/bitcoin.png')
    elif key == 1:
        static_image = cv2.imread('CV Game/Assets/ethereum.png')
    elif key == 2:
        static_image = cv2.imread('CV Game/Assets/tax.png')

    # Resize the static image to match desired dimensions
    static_height, static_width = static_image.shape[:2]
    aspect_ratio = static_width / static_height
    desired_static_height = int(desired_static_width / aspect_ratio)
    resized_static_image = cv2.resize(static_image, (desired_static_width, desired_static_height))
    center_x = x_offset + desired_static_width // 2
    center_y = y_offset + desired_static_height // 2
    
    print(f"Center coordinates: x={center_x}, y={center_y}")  # Print the center coordinates
    # Overlay the static image on the webcam frame (making it opaque)
    combined_frame = frame.copy()
    combined_frame[y_offset:y_offset + desired_static_height, x_offset:x_offset + desired_static_width] = resized_static_image
    st = time.time()
    while el <= 1.0:
        cv2.circle(combined_frame,(center_x,center_y),1,(0,0,255),-4)
        stp = time.time()
        el = stp - st
    # Display the combined frame
    combined_frame = cv2.flip(combined_frame,1 )
    cv2.imshow('Webcam', combined_frame)
    elapsed = time.time()
    timer = elapsed - start
    results = model.predict(combined_frame, stream = True,conf=0.1)                # run prediction on img
    for result in results:                                         # iterate results
        boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
        for box in boxes:                                          # iterate boxes
            r = box.xyxy[0].astype(int)
            xmin = r[0]
            ymin = r[1]
            xmax = r[2]
            ymax = r[3]                            # get corner points as int
            print(r)
    if key !=2:
        if xmin<center_x<xmax and ymin<center_y<ymax:
            score+=10
    else:
        if xmin<center_x<xmax and ymin<center_y<ymax:
            score+=10
    # model.predict(source = '0',show = True)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
print("Your Score was: ",score)
