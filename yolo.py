
import cv2
import numpy as np

def detect_image(image):
    detections = [{"label": "person", "confidence": 0.95}]
    output_image = image.copy()
    cv2.putText(output_image, "person", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return output_image, detections

def detect_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('processed_video.mp4', fourcc, 20.0, (640,480))
    detections = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        detections.append({"label": "car", "confidence": 0.87})
        cv2.putText(frame, "car", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        out.write(frame)
    cap.release()
    out.release()
    return 'processed_video.mp4', detections
