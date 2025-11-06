import cv2

# ESP32-CAM Stream URL
url = "http://10.119.57.249"   # Replace with your own stream link
cap = cv2.VideoCapture("http://10.119.57.249/stream")

# Check if the connection is successful
if not cap.isOpened():
    print("❌ Unable to connect to ESP32-CAM stream.")
    exit()

# Set up video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')   # Codec for .avi format
out = cv2.VideoWriter('live_feed.avi', fourcc, 20.0, (640, 480))

print("✅ Recording started. Press 'Q' to stop...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠ Frame not received. Check camera connection.")
        break

    # Save each frame to the video file
    out.write(frame)

    # Display live video feed
    cv2.imshow('ESP32-CAM Live Feed (Recording)', frame)

    # Stop when user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Recording stopped by user.")
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()
print("💾 Video saved successfully as 'live_feed.avi'")
