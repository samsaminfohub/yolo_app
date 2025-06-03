import streamlit as st
from object_detection import YOLODetector
from database import Database
from mlflow_utils import MLflowLogger
from config import UPLOAD_FOLDER, OUTPUT_FOLDER
import os
import json
from PIL import Image
import pandas as pd

# Initialiser les composants
detector = YOLODetector()
db = Database()
mlflow_logger = MLflowLogger()

# Configuration de la page Streamlit
st.set_page_config(page_title="YOLO Object Detection", layout="wide")
st.title("YOLO Object Detection with OpenCV")

# Section de téléchargement et détection
st.header("Upload Image for Detection")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Sauvegarder le fichier uploadé
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Afficher l'image originale
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Original Image", use_column_width=True)
    
    # Détection d'objets
    with st.spinner("Detecting objects..."):
        try:
            results = detector.detect_objects(file_path)
            
            # Enregistrer dans MLflow
            run_id = mlflow_logger.log_detection(
                uploaded_file.name, 
                results["objects"], 
                results["output_path"]
            )
            
            # Enregistrer dans la base de données
            detection_id = db.insert_detection(
                uploaded_file.name,
                json.dumps(results["objects"]),
                results["output_path"],
                run_id
            )
            
            # Afficher les résultats
            with col2:
                st.image(results["output_path"], caption="Detected Objects", use_column_width=True)
                
            st.success("Detection completed successfully!")
            
            # Afficher les métriques
            st.subheader("Detection Metrics")
            metrics_data = {
                "Metric": ["Processing Time", "Objects Detected", "Image Width", "Image Height"],
                "Value": [
                    f"{results['processing_time']:.2f} seconds",
                    len(results["objects"]),
                    f"{results['image_size']['width']}px",
                    f"{results['image_size']['height']}px"
                ]
            }
            st.table(pd.DataFrame(metrics_data))
            
            # Afficher les objets détectés
            st.subheader("Detected Objects")
            if results["objects"]:
                objects_data = []
                for obj in results["objects"]:
                    objects_data.append([
                        obj["class"],
                        f"{obj['confidence']:.2%}",
                        obj["box"]["x"],
                        obj["box"]["y"],
                        obj["box"]["width"],
                        obj["box"]["height"]
                    ])
                
                df = pd.DataFrame(
                    objects_data,
                    columns=["Class", "Confidence", "X", "Y", "Width", "Height"]
                )
                st.dataframe(df)
            else:
                st.warning("No objects detected!")
                
        except Exception as e:
            st.error(f"Error during detection: {str(e)}")

# Afficher l'historique des détections
st.header("Detection History")
recent_detections = db.get_recent_detections(5)

if recent_detections:
    history_data = []
    for detection in recent_detections:
        detection_id, filename, detection_time, objects_detected, output_path = detection
        num_objects = len(json.loads(objects_detected)) if objects_detected else 0
        history_data.append([
            detection_id,
            filename,
            detection_time.strftime("%Y-%m-%d %H:%M:%S"),
            num_objects,
            output_path
        ])
    
    history_df = pd.DataFrame(
        history_data,
        columns=["ID", "Filename", "Detection Time", "Objects Detected", "Output Path"]
    )
    st.dataframe(history_df)
else:
    st.info("No detection history available.")

# Fermer la connexion à la base de données
db.close()