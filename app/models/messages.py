import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Status(enum.Enum):
    ONLINE = "online"
    LEFT = "left"


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    message = Column(String, nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(Status), nullable=False)
    room_id = Column(Integer, ForeignKey("room.id", ondelete="CASCADE"), nullable=False)
    room = relationship("Room")
