"""
Chatbot endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from backend.app.db.base import get_db, ChatHistory
from backend.app.core.security import get_current_user
from backend.app.core.logging import get_logger
from backend.app.ml.nlp.biobert_model import get_biobert_model

logger = get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message schema."""
    message: str


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    context: Optional[dict] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(
    message_data: ChatMessage,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat with the dermatology AI assistant.
    
    Currently uses rule-based responses.
    In production: Integrate with OpenAI GPT-4 or fine-tuned medical LLM.
    """
    try:
        user_message = message_data.message.lower()
        
        # Simple rule-based chatbot (replace with GPT/LLM integration)
        response = _generate_response(user_message)
        
        # Extract symptoms using NLP
        biobert = get_biobert_model()
        symptoms = biobert.extract_symptoms(user_message)
        severity = biobert.classify_severity(user_message)
        
        context = {
            "symptoms": symptoms,
            "severity": severity
        }
        
        # Save chat history
        chat_record = ChatHistory(
            user_id=current_user["user_id"],
            message=message_data.message,
            response=response,
            context=context
        )
        db.add(chat_record)
        db.commit()
        
        logger.info(f"Chat interaction for user: {current_user['user_id']}")
        
        return {
            "response": response,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chat failed"
        )


def _generate_response(message: str) -> str:
    """
    Generate chatbot response.
    
    This is a simple rule-based implementation.
    Replace with OpenAI GPT-4 or fine-tuned medical LLM for production.
    """
    # Check for common queries
    if "mole" in message or "lesion" in message:
        return (
            "I can help analyze skin lesions. For the best assessment:\n"
            "1. Take a clear, well-lit photo of the lesion\n"
            "2. Use natural lighting if possible\n"
            "3. Ensure the lesion is in focus\n"
            "4. Upload the image for AI analysis\n\n"
            "Please note: This AI analysis is not a replacement for professional medical advice."
        )
    
    elif "melanoma" in message or "cancer" in message:
        return (
            "Melanoma is a serious form of skin cancer. Warning signs include:\n"
            "- Asymmetry in mole shape\n"
            "- Irregular borders\n"
            "- Multiple colors\n"
            "- Diameter larger than 6mm\n"
            "- Changes over time (Evolution)\n\n"
            "If you're concerned, please upload an image for analysis and consult a dermatologist."
        )
    
    elif "how" in message and "photo" in message:
        return (
            "To take a good photo for analysis:\n"
            "1. Use natural daylight or bright indoor lighting\n"
            "2. Hold camera 6-12 inches from the skin\n"
            "3. Make sure the image is in focus\n"
            "4. Avoid flash if possible\n"
            "5. Include a reference object (like a ruler) if available\n"
            "6. Take photos from multiple angles if needed"
        )
    
    elif "pain" in message or "itching" in message or "bleeding" in message:
        return (
            "Symptoms like pain, itching, or bleeding from a skin lesion should be evaluated by a healthcare professional. "
            "These could be signs that require immediate attention. Please consider uploading an image for AI analysis "
            "and scheduling an appointment with a dermatologist soon."
        )
    
    elif "thank" in message:
        return "You're welcome! Feel free to ask any questions about skin conditions or how to use this tool."
    
    elif "help" in message:
        return (
            "I'm here to help with dermatology-related questions. I can:\n"
            "- Guide you on taking good photos for analysis\n"
            "- Explain skin conditions\n"
            "- Answer questions about the ABCDE rule for melanoma\n"
            "- Help you understand your AI analysis results\n\n"
            "What would you like to know?"
        )
    
    else:
        return (
            "I'm a dermatology AI assistant. I can help you with skin condition analysis. "
            "Please upload a clear image of the skin area you're concerned about, "
            "and I'll provide an AI-powered analysis. Remember, this is not a substitute "
            "for professional medical advice. Always consult with a qualified dermatologist."
        )
