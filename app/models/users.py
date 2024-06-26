from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, nullable=True)
    users_room = relationship("UsersRoom")
