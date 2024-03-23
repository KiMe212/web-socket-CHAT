from sqlalchemy import Column, ForeignKey, Integer, String

from app.database import Base


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)
