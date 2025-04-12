from datetime import date
from sqlalchemy import Column, Date, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UsageRecord(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    date = Column(Date, default=date.today)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="usage_records")
    
    # Unique constraint per user per day
    __table_args__ = (
        # SQLAlchemy syntax for unique constraint
        # UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
