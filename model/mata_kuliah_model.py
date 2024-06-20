from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime
from typing import List
from datetime import datetime

from . import Base

class MataKuliah(Base):
    __tablename__ = "mata_kuliah"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    kd_mata_kuliah: Mapped[str] = mapped_column(String(50), nullable=True)
    nama_mata_kuliah: Mapped[str] = mapped_column(String(47), nullable=True)
    nama_mata_kuliah_inggris: Mapped[str] = mapped_column(String(84), nullable=True)
    sks: Mapped[int] = mapped_column(nullable=True)
    semester: Mapped[str] = mapped_column(String(50), nullable=True)
    tingkat_mata_kuliah: Mapped[int] = mapped_column(nullable=True)
    is_lab: Mapped[bool] = mapped_column(Boolean, nullable=True)
    index_minimum: Mapped[bool] = mapped_column(Boolean, nullable=True)
    id_program_studi: Mapped[int] = mapped_column(nullable=True)
    nama_prodi: Mapped[str] = mapped_column(String(50), nullable=True)
    nama_prodi_en: Mapped[str] = mapped_column(String(50), nullable=True)

    pengajaran: Mapped[List["Pengajaran"]] = relationship("Pengajaran", back_populates="mata_kuliah", lazy="selectin")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

from .pengajaran_model import Pengajaran