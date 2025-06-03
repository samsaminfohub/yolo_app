import mlflow
from config import MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME
import time
from datetime import datetime

class MLflowLogger:
    def __init__(self):
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
        
    def start_run(self):
        self.run = mlflow.start_run()
        self.start_time = time.time()
        return self.run.info.run_id
        
    def log_params(self, params):
        mlflow.log_params(params)
        
    def log_metrics(self, metrics):
        mlflow.log_metrics(metrics)
        
    def log_artifact(self, artifact_path):
        mlflow.log_artifact(artifact_path)
        
    def end_run(self):
        duration = time.time() - self.start_time
        mlflow.log_metric("duration_seconds", duration)
        mlflow.end_run()
        
    def log_detection(self, filename, objects_detected, output_path):
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("filename", filename)
            mlflow.log_param("detection_time", datetime.now().isoformat())
            
            # Log metrics (count of each object detected)
            object_counts = {}
            for obj in objects_detected:
                obj_class = obj["class"]
                object_counts[obj_class] = object_counts.get(obj_class, 0) + 1
                
            for obj_class, count in object_counts.items():
                mlflow.log_metric(f"count_{obj_class}", count)
                
            # Log artifact (output image)
            if output_path:
                mlflow.log_artifact(output_path)
                
            return mlflow.active_run().info.run_id