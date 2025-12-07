import cv2
import numpy as np
from ultralytics import YOLO

from bytetrack_tracker import ByteTracker
from utils.speed_estimation import SpeedEstimator
from utils.line_crossing import LineCounter
from utils.calibration import Calibration

# -------------------------
# Video Path
# -------------------------
video_path = r"C:\Users\USER\Desktop\vehicle speed tracking\traffic.mp4"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)

# -------------------------
# Calibration (EDIT THIS)
# -------------------------
# Measure pixels between two known road points.
cal = Calibration(real_distance_meters=10, pixel_distance=200)
meters_per_pixel = cal.get_factor()

# -------------------------
# Setup Modules
# -------------------------
tracker = ByteTracker()
speed = SpeedEstimator(meters_per_pixel, fps)
counter = LineCounter(y_line=400)

model = YOLO("yolov8n.pt")  # auto-download

# Vehicle classes
VEHICLES = [2, 3, 5, 7]

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls)
        if cls in VEHICLES:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            detections.append([x1, y1, x2, y2])

    tracks = tracker.update(detections)

    # Draw line
    cv2.line(frame, (0, 400), (1920, 400), (255, 255, 0), 2)

    for tr in tracks:
        x1, y1, x2, y2 = tr.box
        track_id = tr.id
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # SPEED
        speed_kmph = speed.update(track_id, cx, cy)

        # COUNTING
        if counter.check(track_id, cy):
            count += 1

        # OVERSPEED ALERT
        alert = ""
        if speed_kmph > 60:
            alert = "OVERSPEED!"

        # Draw box
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id} {speed_kmph:.1f} km/h {alert}",
                    (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255) if alert else (255, 255, 255), 2)

    # Display Count
    cv2.putText(frame, f"Vehicles Passed: {count}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    cv2.imshow("Vehicle Analytics - ByteTrack", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
