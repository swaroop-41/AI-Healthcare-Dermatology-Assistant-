"""
Validation utilities.
"""

import re
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import io

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None


async def validate_image_upload(file: UploadFile, max_size_mb: int = 10) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded image file.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file type
    if not file.content_type.startswith('image/'):
        return False, "File must be an image"
    
    # Check file size
    content = await file.read()
    await file.seek(0)  # Reset file pointer
    
    size_mb = len(content) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"Image size must be less than {max_size_mb}MB"
    
    # Try to open image
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
        
        # Check dimensions (reasonable limits)
        if image.size[0] > 4000 or image.size[1] > 4000:
            return False, "Image dimensions too large (max 4000x4000 pixels)"
        
        if image.size[0] < 100 or image.size[1] < 100:
            return False, "Image dimensions too small (min 100x100 pixels)"
        
    except Exception as e:
        logger.error(f"Image validation error: {e}")
        return False, "Invalid image file"
    
    return True, None


def calculate_image_quality_score(image_path: str) -> float:
    """
    Calculate image quality score (0-1).
    
    Factors:
    - Resolution
    - Sharpness
    - Lighting
    """
    try:
        image = Image.open(image_path)
        
        # Simple quality metrics
        width, height = image.size
        resolution_score = min((width * height) / (1024 * 1024), 1.0)  # Normalize to 1MP
        
        # Placeholder for more advanced metrics (could use opencv for blur detection, etc.)
        quality_score = resolution_score * 0.8  # Conservative estimate
        
        return min(max(quality_score, 0.0), 1.0)
        
    except Exception as e:
        logger.error(f"Quality score calculation error: {e}")
        return 0.5  # Default medium quality
