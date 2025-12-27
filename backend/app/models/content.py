from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(50), nullable=False)  # 'text' or 'image'
    content = Column(Text, nullable=True)  # For text content
    file_path = Column(String(255), nullable=True)  # For file paths
    is_approved = Column(Boolean, default=False)
    moderation_result = Column(Text, nullable=True)  # JSON string of moderation results
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    user = relationship("User", back_populates="contents")
    moderation_logs = relationship("ModerationLog", back_populates="content")