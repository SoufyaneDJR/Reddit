import cv2
import numpy as np

import time
import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNet("Football-players-detection/files/yolov3.weights", "Football-players-detection/files/yolov3.cfg")

# Set parameters for ball detection
confidence_threshold = 0.5
nms_threshold = 0.4
output_layers = net.getUnconnectedOutLayersNames()

# Load video
cap = cv2.VideoCapture('Football-players-detection/data/test.mp4')

while cap.isOpened():
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Pass the frame through the network
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Process the detections for ball
    height, width, _ = frame.shape
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > confidence_threshold and class_id == 0:  # Ball class_id is 0
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)

    # Draw bounding boxes for ball detections
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Ball Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
