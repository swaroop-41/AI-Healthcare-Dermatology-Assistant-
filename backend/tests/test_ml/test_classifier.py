"""
Test skin classifier.
"""

import pytest
import torch
from backend.app.ml.dermatology.skin_classifier import SkinClassifier


def test_classifier_initialization():
    """Test classifier can be initialized."""
    classifier = SkinClassifier()
    assert classifier is not None
    assert classifier.model is not None


def test_classifier_classes():
    """Test classifier has correct classes."""
    classifier = SkinClassifier()
    assert len(classifier.CLASSES) == 8
    assert 'MEL' in classifier.CLASSES
    assert 'BCC' in classifier.CLASSES


def test_preprocess_image():
    """Test image preprocessing (would need actual image file)."""
    # This is a placeholder - in real tests you'd use a sample image
    pass
