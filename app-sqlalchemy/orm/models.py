from ..adapters.database_connection import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
