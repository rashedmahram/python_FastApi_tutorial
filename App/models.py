

from psycopg2 import Timestamp
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, null, text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='true', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=True, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
