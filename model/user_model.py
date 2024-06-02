#/model/kelas_model.py
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime, event, Boolean
from datetime import datetime
from typing import List

from . import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True) 
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False) 
    image_picture: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now) 
    
    dosen: Mapped[List["Dosen"]] = relationship("Dosen", back_populates="users", lazy="selectin")
 
from .dosen_model import Dosen

@event.listens_for(User, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()