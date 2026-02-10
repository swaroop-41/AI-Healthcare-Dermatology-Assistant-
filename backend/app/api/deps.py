"""
API dependencies.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.core.security import get_current_user


def get_db_session() -> Generator:
    """Database session dependency."""
    return get_db()


def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Get current active user dependency."""
    if not current_user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user
