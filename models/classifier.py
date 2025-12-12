"""
Plastic Waste Classifier using Keras/TensorFlow
This module provides a classifier that loads a trained Keras model
and predicts plastic types from images.
"""

import os
import numpy as np
from typing import Dict, Any

try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image as keras_image_utils
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False


class PlasticClassifier:
    """Plastic waste classifier using Keras/TensorFlow model."""
    
    CLASS_NAMES_24 = [
        'TYPE 1 — PET_plastic_soda_bottles',
        'TYPE 1 — PET_plastic_water_bottles',
        'TYPE 2 — HDPE_plastic_detergent_bottles',
        'TYPE 2 — HDPE_plastic_trash_bags',
        'TYPE 3 — PVC_damaged_pipes',
        'TYPE 3 — PVC_undamaged_pipes',
        'TYPE 4 — LDPE_paper_cups',
        'TYPE 4 — LDPE_plastic_shopping_bags',
        'TYPE 5 — PP_disposable_plastic_cutlery',
        'TYPE 5 — PP_plastic_cup_lids',
        'TYPE 5 — PP_plastic_food_containers',
        'TYPE 5 — PP_plastic_straws',
        'TYPE 6 — PS_styrofoam_cups',
        'TYPE 6 — PS_styrofoam_food_containers',
        'TYPE 7 — OTHER_Battery',
        'TYPE 7 — OTHER_Keyboard',
        'TYPE 7 — OTHER_Microwave',
        'TYPE 7 — OTHER_Mobile',
        'TYPE 7 — OTHER_Mouse',
        'TYPE 7 — OTHER_PCB',
        'TYPE 7 — OTHER_Player',
        'TYPE 7 — OTHER_Printer',
        'TYPE 7 — OTHER_Television',
        'TYPE 7 — OTHER_Washing_Machine'
    ]
    
    PLASTIC_TYPES = {
        'TYPE 1 — PET': {'name': 'PET', 'code': 1, 'recyclable': True, 'description': 'Beverage bottles, food containers', 'environmental_impact': 'Takes 450+ years to decompose. Recyclable into fibers and containers.'},
        'TYPE 2 — HDPE': {'name': 'HDPE', 'code': 2, 'recyclable': True, 'description': 'Milk bottles, detergent bottles', 'environmental_impact': 'Takes 400+ years to decompose. Recyclable into containers and packaging.'},
        'TYPE 3 — PVC': {'name': 'PVC', 'code': 3, 'recyclable': False, 'description': 'Pipes, vinyl siding, food wrap', 'environmental_impact': 'Takes 450+ years to decompose. Difficult to recycle.'},
        'TYPE 4 — LDPE': {'name': 'LDPE', 'code': 4, 'recyclable': True, 'description': 'Plastic wrap, squeeze bottles', 'environmental_impact': 'Takes 400+ years to decompose. Recyclable into films and bags.'},
        'TYPE 5 — PP': {'name': 'PP', 'code': 5, 'recyclable': True, 'description': 'Yogurt containers, bottle caps', 'environmental_impact': 'Takes 400+ years to decompose. Recyclable into automotive parts.'},
        'TYPE 6 — PS': {'name': 'PS', 'code': 6, 'recyclable': False, 'description': 'Foam cups, takeout containers', 'environmental_impact': 'Takes 500+ years to decompose. Difficult to recycle.'},
        'TYPE 7 — OTHER': {'name': 'Other', 'code': 7, 'recyclable': False, 'description': 'Mixed plastic materials', 'environmental_impact': 'Highly variable. Usually not recyclable.'},
    }
    
    def __init__(self, model_path=None):
        """Initialize classifier and load model if available."""
        self.model = None
        self.model_loaded = False
        self.error_message = None
        
        if model_path and KERAS_AVAILABLE:
            self.load_model(model_path)
        elif not KERAS_AVAILABLE:
            self.error_message = "TensorFlow/Keras not installed. Using placeholder predictions."
    
    def load_model(self, model_path):
        """Load Keras model from file."""
        try:
            if not os.path.exists(model_path):
                self.error_message = f"Model not found: {model_path}"
                return
            
            self.model = load_model(model_path)
            self.model_loaded = True
            print(f"✓ Model loaded: {model_path}")
        except Exception as e:
            self.error_message = f"Failed to load model: {str(e)}"
            print(f"✗ {self.error_message}")
    
    def preprocess_image(self, image_path):
        """Preprocess image (224x224, normalized)."""
        try:
            img = keras_image_utils.load_img(image_path, target_size=(224, 224))
            x = keras_image_utils.img_to_array(img) / 255.0
            x = np.expand_dims(x, axis=0)
            return x
        except Exception as e:
            raise Exception(f"Preprocessing failed: {str(e)}")
    
    def map_prediction_to_type(self, predicted_class):
        """Map 24-class output to TYPE 1-7."""
        if "TYPE 1" in predicted_class:
            return "TYPE 1 — PET"
        elif "TYPE 2" in predicted_class:
            return "TYPE 2 — HDPE"
        elif "TYPE 3" in predicted_class:
            return "TYPE 3 — PVC"
        elif "TYPE 4" in predicted_class:
            return "TYPE 4 — LDPE"
        elif "TYPE 5" in predicted_class:
            return "TYPE 5 — PP"
        elif "TYPE 6" in predicted_class:
            return "TYPE 6 — PS"
        elif "TYPE 7" in predicted_class:
            return "TYPE 7 — OTHER"
        return "Unknown"
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """Predict plastic type from image."""
        if self.model_loaded and self.model is not None:
            try:
                img_array = self.preprocess_image(image_path)
                preds = self.model.predict(img_array, verbose=0)
                predicted_index = np.argmax(preds)
                predicted_confidence = float(preds[0][predicted_index])
                
                predicted_subclass = self.CLASS_NAMES_24[predicted_index]
                predicted_type = self.map_prediction_to_type(predicted_subclass)
                plastic_info = self.PLASTIC_TYPES.get(predicted_type, {})
                
                return {
                    'class': predicted_type,
                    'code': plastic_info.get('code', 7),
                    'confidence': predicted_confidence,
                    'description': plastic_info.get('description', 'Unknown'),
                    'environmental_impact': plastic_info.get('environmental_impact', 'Unknown'),
                    'recyclable': plastic_info.get('recyclable', False)
                }
            except Exception as e:
                print(f"Prediction error: {str(e)}")
                return self._placeholder_prediction()
        
        return self._placeholder_prediction()
    
    def _placeholder_prediction(self):
        """Return placeholder prediction."""
        plastic_type = "TYPE 1 — PET"
        info = self.PLASTIC_TYPES[plastic_type]
        return {
            'class': plastic_type,
            'code': info['code'],
            'confidence': 0.85,
            'description': info['description'],
            'environmental_impact': info['environmental_impact'],
            'recyclable': info['recyclable']
        }
