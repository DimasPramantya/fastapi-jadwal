#/model/kelas_model.py
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, DateTime, event
from datetime import datetime
from typing import List

from . import Base

class Kelas(Base):
    __tablename__ = "kelas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nama_kelas: Mapped[str] = mapped_column(String(10), nullable=True)
    id_prodi: Mapped[int] = mapped_column(nullable=True)
    nama_prodi: Mapped[str] = mapped_column(String(22), nullable=True) 
    shift: Mapped[str] = mapped_column(String(255), nullable=True) 
    kuota: Mapped[int] = mapped_column(nullable=True)
    
    id_dosen_wali: Mapped[int] = mapped_column(ForeignKey("dosen.id"), nullable = True)
    dosen: Mapped["Dosen"] = relationship("Dosen", back_populates="kelas", lazy="selectin")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now) 
    
    pengajaran: Mapped[List["Pengajaran"]] = relationship("Pengajaran", back_populates="kelas", lazy="selectin")
 
from .dosen_model import Dosen
from .pengajaran_model import Pengajaran 

@event.listens_for(Kelas, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()