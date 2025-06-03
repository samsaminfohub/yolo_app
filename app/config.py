import os
from os.path import join, dirname
from dotenv import load_dotenv

# Charger les variables d'environnement
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Chemins des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "utils", "models", "yolov3.weights")
CONFIG_PATH = os.path.join(BASE_DIR, "utils", "models", "yolov3.cfg")
CLASSES_PATH = os.path.join(BASE_DIR, "utils", "models", "coco.names")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "utils", "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "utils", "outputs")

# Paramètres YOLO
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4

# Paramètres MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MLFLOW_EXPERIMENT_NAME = "YOLO Object Detection"

# Paramètres PostgreSQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "database": os.getenv("POSTGRES_DB", "yolo_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    "port": os.getenv("DB_PORT", "5432")
}

# Créer les dossiers s'ils n'existent pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)