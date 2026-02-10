"""
Skin lesion classifier using ResNet18 and ensemble models.
"""

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from typing import Dict, List, Tuple, Optional
import os

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class SkinClassifier:
    """Skin lesion classifier with support for ensemble models."""
    
    # Skin condition classes
    CLASSES = ['AK', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'SCC', 'VASC']
    
    CLASS_NAMES = {
        'AK': 'Actinic Keratosis',
        'BCC': 'Basal Cell Carcinoma',
        'BKL': 'Benign Keratosis',
        'DF': 'Dermatofibroma',
        'MEL': 'Melanoma',
        'NV': 'Melanocytic Nevus',
        'SCC': 'Squamous Cell Carcinoma',
        'VASC': 'Vascular Lesion'
    }
    
    def __init__(self, model_path: Optional[str] = None, use_ensemble: bool = False):
        """Initialize the classifier."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path or settings.MODEL_PATH
        self.use_ensemble = use_ensemble
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Load model
        self.model = self._load_model()
        logger.info(f"Skin classifier loaded on {self.device}")
    
    def _load_model(self) -> nn.Module:
        """Load the trained model."""
        try:
            # Create ResNet18 model
            model = models.resnet18(pretrained=False)
            num_features = model.fc.in_features
            model.fc = nn.Linear(num_features, len(self.CLASSES))
            
            # Load weights if available
            if os.path.exists(self.model_path):
                model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                logger.info(f"Loaded model weights from {self.model_path}")
            else:
                logger.warning(f"Model weights not found at {self.model_path}. Using untrained model.")
            
            model.to(self.device)
            model.eval()
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """Preprocess image for model input."""
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0)
            return image_tensor.to(self.device)
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def predict(self, image_path: str) -> Dict:
        """
        Predict skin condition from image.
        
        Returns:
            Dictionary containing prediction results
        """
        try:
            # Preprocess image
            image_tensor = self.preprocess_image(image_path)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
            
            # Get top 3 predictions
            top_probs, top_indices = torch.topk(probabilities[0], k=min(3, len(self.CLASSES)))
            
            all_predictions = []
            for prob, idx in zip(top_probs, top_indices):
                class_label = self.CLASSES[idx.item()]
                all_predictions.append({
                    "class": class_label,
                    "name": self.CLASS_NAMES[class_label],
                    "confidence": float(prob.item())
                })
            
            primary_class = self.CLASSES[predicted_idx.item()]
            
            result = {
                "primary_prediction": primary_class,
                "primary_name": self.CLASS_NAMES[primary_class],
                "confidence": float(confidence.item()),
                "all_predictions": all_predictions,
                "ensemble_consensus": None  # Will be set if using ensemble
            }
            
            logger.info(f"Prediction: {primary_class} with confidence {confidence.item():.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise
    
    def get_feature_vector(self, image_path: str) -> np.ndarray:
        """Extract feature vector from the model (for ensemble or risk assessment)."""
        try:
            image_tensor = self.preprocess_image(image_path)
            
            # Remove final classification layer to get features
            features_model = nn.Sequential(*list(self.model.children())[:-1])
            
            with torch.no_grad():
                features = features_model(image_tensor)
                features = features.squeeze().cpu().numpy()
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            raise


# Global classifier instance
_classifier_instance = None


def get_classifier() -> SkinClassifier:
    """Get or create global classifier instance."""
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = SkinClassifier()
    return _classifier_instance
