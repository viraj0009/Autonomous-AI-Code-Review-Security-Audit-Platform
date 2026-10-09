from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    status = Column(String(40), default="completed")
    findings_json = Column(Text, default="[]")
    ai_report = Column(Text, default="")
    suggested_fix = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)