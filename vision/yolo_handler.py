# vision/yolo_handler.py

"""
Modulo: yolo_handler.py
Descrizione: Riconoscimento oggetti con YOLOv5/YOLOv8 tramite OpenCV per Mercurius∞.
"""

from typing import List
import torch
import numpy as np

# Caricamento modello YOLO (richiede modello pre-addestrato disponibile localmente)
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)
except Exception as e:
    print("⚠️ Errore nel caricamento del modello YOLO:", e)
    model = None


def detect_objects(image: np.ndarray) -> List[str]:
    """
    Rileva oggetti in un'immagine e restituisce le etichette.
    """
    if model is None:
        return []

    results = model(image)
    labels = results.pandas().xyxy[0]['name'].tolist()
    return labels
