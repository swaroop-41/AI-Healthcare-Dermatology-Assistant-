"""
ABCDE rule analyzer for melanoma detection.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Dict
import math

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class ABCDEAnalyzer:
    """Analyzes skin lesions using the ABCDE rule."""
    
    def __init__(self):
        """Initialize ABCDE analyzer."""
        pass
    
    def analyze(self, image_path: str) -> Dict[str, float]:
        """
        Analyze image using ABCDE criteria.
        
        Returns:
            Dictionary with ABCDE scores
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            # Convert to grayscale and apply thresholding to segment lesion
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                logger.warning("No lesion detected in image")
                return self._default_scores()
            
            # Get largest contour (assume it's the lesion)
            lesion_contour = max(contours, key=cv2.contourArea)
            
            # Calculate ABCDE features
            asymmetry_score = self._calculate_asymmetry(lesion_contour, thresh)
            border_score = self._calculate_border_irregularity(lesion_contour)
            color_score = self._calculate_color_variation(image, lesion_contour)
            diameter_mm = self._estimate_diameter(lesion_contour)
            
            scores = {
                "asymmetry": round(asymmetry_score, 2),
                "border": round(border_score, 2),
                "color": round(color_score, 2),
                "diameter_mm": round(diameter_mm, 2),
                "evolution": "unknown"  # Requires historical images
            }
            
            logger.info(f"ABCDE scores: {scores}")
            return scores
            
        except Exception as e:
            logger.error(f"Error in ABCDE analysis: {e}")
            return self._default_scores()
    
    def _default_scores(self) -> Dict[str, float]:
        """Return default scores when analysis fails."""
        return {
            "asymmetry": 0.5,
            "border": 0.5,
            "color": 0.5,
            "diameter_mm": 5.0,
            "evolution": "unknown"
        }
    
    def _calculate_asymmetry(self, contour: np.ndarray, binary_image: np.ndarray) -> float:
        """
        Calculate asymmetry score (0-1).
        Higher score indicates more asymmetry.
        """
        try:
            # Get moments and centroid
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return 0.5
            
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Create mask
            mask = np.zeros_like(binary_image)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            
            # Split along major axis
            height, width = binary_image.shape
            half1 = mask[:, :cx]
            half2 = mask[:, cx:]
            
            # Calculate difference
            min_width = min(half1.shape[1], half2.shape[1])
            if min_width > 0:
                diff = np.abs(half1[:, :min_width].astype(float) - 
                             np.flip(half2[:, :min_width], axis=1).astype(float))
                asymmetry = np.mean(diff) / 255.0
                return min(asymmetry * 2, 1.0)  # Normalize to 0-1
            
            return 0.5
            
        except Exception as e:
            logger.error(f"Error calculating asymmetry: {e}")
            return 0.5
    
    def _calculate_border_irregularity(self, contour: np.ndarray) -> float:
        """
        Calculate border irregularity score (0-1).
        Higher score indicates more irregular borders.
        """
        try:
            # Calculate perimeter and area
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            
            if area == 0:
                return 0.5
            
            # Circularity (4π*area/perimeter²)
            # Perfect circle = 1, irregular shape < 1
            circularity = (4 * math.pi * area) / (perimeter ** 2)
            
            # Convert to irregularity score (1 - circularity)
            irregularity = 1.0 - circularity
            
            # Normalize to 0-1 range
            return min(max(irregularity, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating border irregularity: {e}")
            return 0.5
    
    def _calculate_color_variation(self, image: np.ndarray, contour: np.ndarray) -> float:
        """
        Calculate color variation score (0-1).
        Higher score indicates more color variety.
        """
        try:
            # Create mask
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            
            # Extract lesion region
            lesion_pixels = image[mask > 0]
            
            if len(lesion_pixels) == 0:
                return 0.5
            
            # Calculate color variance in each channel
            variances = np.var(lesion_pixels, axis=0)
            avg_variance = np.mean(variances)
            
            # Normalize (empirically determined threshold)
            color_score = min(avg_variance / 2000.0, 1.0)
            
            return color_score
            
        except Exception as e:
            logger.error(f"Error calculating color variation: {e}")
            return 0.5
    
    def _estimate_diameter(self, contour: np.ndarray, pixels_per_mm: float = 10.0) -> float:
        """
        Estimate diameter in millimeters.
        
        Note: pixels_per_mm is an approximation. In production, this should be
        calibrated based on camera distance and reference object.
        """
        try:
            # Get minimum enclosing circle
            (x, y), radius = cv2.minEnclosingCircle(contour)
            diameter_pixels = 2 * radius
            
            # Convert to mm (approximate - needs calibration)
            diameter_mm = diameter_pixels / pixels_per_mm
            
            return diameter_mm
            
        except Exception as e:
            logger.error(f"Error estimating diameter: {e}")
            return 5.0


# Global analyzer instance
_analyzer_instance = None


def get_abcde_analyzer() -> ABCDEAnalyzer:
    """Get or create global ABCDE analyzer instance."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = ABCDEAnalyzer()
    return _analyzer_instance
