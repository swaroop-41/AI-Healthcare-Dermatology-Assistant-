"""
Grad-CAM++ visualization for explainable AI.
"""

import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image
from typing import Tuple, Optional
import os

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class GradCAMPlusPlus:
    """Grad-CAM++ implementation for visualization."""
    
    def __init__(self, model: torch.nn.Module, target_layer: str = 'layer4'):
        """
        Initialize Grad-CAM++.
        
        Args:
            model: PyTorch model
            target_layer: Name of the target layer for visualization
        """
        self.model = model
        self.model.eval()
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self._register_hooks()
    
    def _register_hooks(self):
        """Register forward and backward hooks."""
        def forward_hook(module, input, output):
            self.activations = output.detach()
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()
        
        # Get target layer
        target_module = dict(self.model.named_modules()).get(self.target_layer)
        if target_module is None:
            logger.warning(f"Target layer {self.target_layer} not found")
            return
        
        target_module.register_forward_hook(forward_hook)
        target_module.register_full_backward_hook(backward_hook)
    
    def generate_cam(self, input_tensor: torch.Tensor, target_class: Optional[int] = None) -> np.ndarray:
        """
        Generate Grad-CAM++ heatmap.
        
        Args:
            input_tensor: Input image tensor
            target_class: Target class index (if None, uses predicted class)
        
        Returns:
            Heatmap as numpy array
        """
        try:
            # Forward pass
            output = self.model(input_tensor)
            
            if target_class is None:
                target_class = output.argmax(dim=1).item()
            
            # Zero gradients
            self.model.zero_grad()
            
            # Backward pass
            target = output[0, target_class]
            target.backward()
            
            # Get gradients and activations
            gradients = self.gradients
            activations = self.activations
            
            # Grad-CAM++ weights calculation
            alpha_num = gradients.pow(2)
            alpha_denom = 2 * gradients.pow(2) + \
                          activations.sum(dim=(2, 3), keepdim=True) * gradients.pow(3)
            alpha_denom = torch.where(alpha_denom != 0.0, alpha_denom, torch.ones_like(alpha_denom))
            alpha = alpha_num / alpha_denom
            
            weights = (alpha * F.relu(gradients)).sum(dim=(2, 3), keepdim=True)
            
            # Generate CAM
            cam = (weights * activations).sum(dim=1, keepdim=True)
            cam = F.relu(cam)
            
            # Normalize
            cam = cam.squeeze().cpu().numpy()
            cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
            
            return cam
            
        except Exception as e:
            logger.error(f"Error generating Grad-CAM: {e}")
            raise
    
    def visualize(
        self,
        image_path: str,
        input_tensor: torch.Tensor,
        output_path: str,
        target_class: Optional[int] = None,
        alpha: float = 0.4
    ) -> str:
        """
        Create and save Grad-CAM visualization overlay.
        
        Args:
            image_path: Path to original image
            input_tensor: Preprocessed image tensor
            output_path: Path to save visualization
            target_class: Target class index
            alpha: Overlay transparency
        
        Returns:
            Path to saved visualization
        """
        try:
            # Generate heatmap
            cam = self.generate_cam(input_tensor, target_class)
            
            # Load original image
            original_image = cv2.imread(image_path)
            original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            h, w = original_image.shape[:2]
            
            # Resize heatmap to match image size
            cam_resized = cv2.resize(cam, (w, h))
            
            # Apply colormap
            heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
            heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
            
            # Overlay heatmap on original image
            overlay = (alpha * heatmap + (1 - alpha) * original_image).astype(np.uint8)
            
            # Save visualization
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            overlay_bgr = cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, overlay_bgr)
            
            logger.info(f"Grad-CAM visualization saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            raise


def create_gradcam_visualization(
    model: torch.nn.Module,
    image_path: str,
    input_tensor: torch.Tensor,
    output_path: str,
    target_class: Optional[int] = None
) -> str:
    """
    Helper function to create Grad-CAM visualization.
    
    Args:
        model: PyTorch model
        image_path: Path to original image
        input_tensor: Preprocessed image tensor
        output_path: Path to save visualization
        target_class: Target class index
    
    Returns:
        Path to saved visualization
    """
    gradcam = GradCAMPlusPlus(model)
    return gradcam.visualize(image_path, input_tensor, output_path, target_class)
