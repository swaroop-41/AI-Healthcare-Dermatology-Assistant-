"""
BioBERT-based medical NLP module (placeholder for production fine-tuned model).
"""

from typing import List, Dict
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class BioBERTModel:
    """BioBERT model for medical text analysis."""
    
    def __init__(self):
        """Initialize BioBERT model."""
        logger.info("BioBERT model initialized (using rule-based fallback)")
        # In production, load fine-tuned BioBERT/ClinicalBERT model
        # from transformers import AutoTokenizer, AutoModel
        # self.tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-v1.1")
        # self.model = AutoModel.from_pretrained("dmis-lab/biobert-v1.1")
    
    def extract_symptoms(self, text: str) -> List[str]:
        """
        Extract symptoms from patient text.
        
        In production: Use fine-tuned BioBERT for NER.
        Current: Rule-based extraction.
        """
        # Simple keyword-based extraction (replace with transformer model)
        symptoms_keywords = [
            'itching', 'pain', 'redness', 'swelling', 'bleeding', 'burning',
            'rash', 'lesion', 'mole', 'spot', 'growth', 'discoloration',
            'scaling', 'crusting', 'oozing'
        ]
        
        text_lower = text.lower()
        found_symptoms = [symptom for symptom in symptoms_keywords if symptom in text_lower]
        
        logger.info(f"Extracted symptoms: {found_symptoms}")
        return found_symptoms
    
    def classify_severity(self, text: str) -> str:
        """Classify symptom severity from text."""
        text_lower = text.lower()
        
        severe_keywords = ['severe', 'extreme', 'unbearable', 'intense', 'terrible']
        moderate_keywords = ['moderate', 'noticeable', 'uncomfortable']
        
        if any(keyword in text_lower for keyword in severe_keywords):
            return "severe"
        elif any(keyword in text_lower for keyword in moderate_keywords):
            return "moderate"
        else:
            return "mild"


class MedicalNER:
    """Medical Named Entity Recognition."""
    
    ENTITY_TYPES = ["SYMPTOM", "DISEASE", "MEDICATION", "DURATION", "SEVERITY"]
    
    def __init__(self):
        """Initialize Medical NER."""
        logger.info("Medical NER initialized")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract medical entities from text.
        
        Returns:
            Dictionary of entity types and their values
        """
        # Placeholder implementation
        # In production: Use fine-tuned BioBERT or SciBERT with NER head
        
        entities = {
            "SYMPTOM": [],
            "DISEASE": [],
            "MEDICATION": [],
            "DURATION": [],
            "SEVERITY": []
        }
        
        # Simple rule-based extraction
        text_lower = text.lower()
        
        # Symptoms
        symptoms = ['itching', 'pain', 'redness', 'bleeding', 'swelling']
        entities["SYMPTOM"] = [s for s in symptoms if s in text_lower]
        
        # Duration keywords
        if 'days' in text_lower or 'weeks' in text_lower:
            entities["DURATION"] = ["temporal"]
        
        logger.info(f"Extracted entities: {entities}")
        return entities


# Global instances
_biobert_model = None
_medical_ner = None


def get_biobert_model() -> BioBERTModel:
    """Get or create global BioBERT model instance."""
    global _biobert_model
    if _biobert_model is None:
        _biobert_model = BioBERTModel()
    return _biobert_model


def get_medical_ner() -> MedicalNER:
    """Get or create global Medical NER instance."""
    global _medical_ner
    if _medical_ner is None:
        _medical_ner = MedicalNER()
    return _medical_ner
