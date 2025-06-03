import cv2
import numpy as np
from config import MODEL_PATH, CONFIG_PATH, CLASSES_PATH, CONFIDENCE_THRESHOLD, NMS_THRESHOLD, OUTPUT_FOLDER
import os
import time

class YOLODetector:
    def __init__(self):
        self.net = cv2.dnn.readNet(MODEL_PATH, CONFIG_PATH)
        self.classes = []
        with open(CLASSES_PATH, "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
            
        layer_names = self.net.getLayerNames()
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        
    def detect_objects(self, img_path):
        # Charger l'image
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Impossible de charger l'image à partir de {img_path}")
            
        height, width, channels = img.shape
        
        # Prétraitement de l'image pour YOLO
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        
        # Mesurer le temps de détection
        start_time = time.time()
        
        # Effectuer la détection
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        duration = time.time() - start_time
        
        # Traiter les résultats
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                
                if confidence > CONFIDENCE_THRESHOLD:
                    # Coordonnées de la boîte englobante
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Coin supérieur gauche
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    
        # Suppression des doublons avec NMS
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        
        # Préparer les résultats
        results = []
        font = cv2.FONT_HERSHEY_PLAIN
        
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]])
                color = self.colors[class_ids[i]]
                
                # Dessiner la boîte et le label
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
                
                # Ajouter aux résultats
                results.append({
                    "class": label,
                    "confidence": float(confidences[i]),
                    "box": {"x": x, "y": y, "width": w, "height": h}
                })
        
        # Sauvegarder l'image avec les détections
        filename = os.path.basename(img_path)
        output_path = os.path.join(OUTPUT_FOLDER, f"detected_{filename}")
        cv2.imwrite(output_path, img)
        
        return {
            "objects": results,
            "output_path": output_path,
            "processing_time": duration,
            "image_size": {"width": width, "height": height}
        }