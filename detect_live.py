import cv2

# Replace with your ESP32-CAM stream URL
url = "http://10.119.57.249"   # Example stream URL
cap = cv2.VideoCapture(url)

# Load pre-trained MobileNetSSD model
net = cv2.dnn.readNetFromCaffe(
    "MobileNetSSD_deploy.prototxt",
    "MobileNetSSD_deploy.caffemodel"
)

# Class labels MobileNetSSD can detect
CLASSES = ["background", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor", "cable wires", "laptop"]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame")
        continue
    
    # Prepare frame for neural network
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.50:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            box = detections[0, 0, i, 3:7] * \
                  np.array([frame.shape[1], frame.shape[0],
                            frame.shape[1], frame.shape[0]])
            (x1, y1, x2, y2) = box.astype("int")

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv2.imshow("ESP32-CAM Live Detection", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
