
import streamlit as st
import numpy as np
import tempfile
import cv2
import mlflow
import os
from yolo import detect_image, detect_video
from db import log_detection
from config import MLFLOW_TRACKING_URI

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

st.title("YOLO Object Detection")

option = st.selectbox("Choose input type", ["Image", "Video"])

if option == "Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        with mlflow.start_run():
            output_img, detections = detect_image(image)
            mlflow.log_param("input_type", "image")
            mlflow.log_metric("objects_detected", len(detections))
            for obj in detections:
                log_detection(obj['label'], uploaded_file.name)
        st.image(output_img, channels="BGR")

elif option == "Video":
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi"])
    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        with mlflow.start_run():
            output_path, detections = detect_video(tfile.name)
            mlflow.log_param("input_type", "video")
            mlflow.log_metric("objects_detected", len(detections))
            for obj in detections:
                log_detection(obj['label'], uploaded_file.name)
        st.video(output_path)
