"""
Fitzpatrick skin tone classification.
"""

import cv2
import numpy as np
from typing import Dict, Tuple

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class SkinToneClassifier:
    """Classify skin tone using Fitzpatrick scale."""
    
    # Fitzpatrick skin types with approximate RGB ranges
    SKIN_TYPES = {
        "Type I": {
            "description": "Pale white skin, always burns, never tans",
            "rgb_range": [(240, 234, 230), (255, 250, 245)]
        },
        "Type II": {
            "description": "White skin, burns easily, tans minimally",
            "rgb_range": [(230, 215, 200), (245, 235, 225)]
        },
        "Type III": {
            "description": "Light brown skin, burns moderately, tans gradually",
            "rgb_range": [(210, 190, 170), (235, 220, 205)]
        },
        "Type IV": {
            "description": "Moderate brown skin, burns minimally, tans well",
            "rgb_range": [(180, 160, 140), (215, 195, 175)]
        },
        "Type V": {
            "description": "Dark brown skin, rarely burns, tans profusely",
            "rgb_range": [(140, 120, 100), (185, 165, 145)]
        },
        "Type VI": {
            "description": "Deeply pigmented dark brown to black, never burns",
            "rgb_range": [(80, 60, 50), (145, 125, 105)]
        }
    }
    
    def __init__(self):
        """Initialize skin tone classifier."""
        pass
    
    def classify(self, image_path: str) -> str:
        """
        Classify Fitzpatrick skin tone from image.
        
        Args:
            image_path: Path to image
        
        Returns:
            Fitzpatrick skin type (e.g., "Type III (Fitzpatrick)")
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                logger.warning(f"Could not load image from {image_path}")
                return "Type III (Fitzpatrick)"
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get average skin tone from image center
            # (Assuming lesion/skin is in center region)
            h, w = image_rgb.shape[:2]
            center_region = image_rgb[h//4:3*h//4, w//4:3*w//4]
            
            # Calculate median RGB values (more robust than mean)
            median_rgb = np.median(center_region.reshape(-1, 3), axis=0)
            
            # Classify based on closest match
            skin_type = self._classify_rgb(median_rgb)
            
            logger.info(f"Classified skin tone: {skin_type}")
            return f"{skin_type} (Fitzpatrick)"
            
        except Exception as e:
            logger.error(f"Error classifying skin tone: {e}")
            return "Type III (Fitzpatrick)"
    
    def _classify_rgb(self, rgb: np.ndarray) -> str:
        """Classify RGB values to Fitzpatrick type."""
        min_distance = float('inf')
        best_type = "Type III"
        
        for skin_type, info in self.SKIN_TYPES.items():
            # Calculate distance to range midpoint
            range_min = np.array(info['rgb_range'][0])
            range_max = np.array(info['rgb_range'][1])
            midpoint = (range_min + range_max) / 2
            
            distance = np.linalg.norm(rgb - midpoint)
            
            if distance < min_distance:
                min_distance = distance
                best_type = skin_type
        
        return best_type


# Global classifier instance
_skin_tone_classifier = None


def get_skin_tone_classifier() -> SkinToneClassifier:
    """Get or create global skin tone classifier instance."""
    global _skin_tone_classifier
    if _skin_tone_classifier is None:
        _skin_tone_classifier = SkinToneClassifier()
    return _skin_tone_classifier
