#/model/dosen_model.py
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy import String, DateTime, event, ForeignKey
from datetime import datetime

from . import Base

class Dosen(Base):
    __tablename__ = "dosen"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nip: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    nidn: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    id_pegawai: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    inisial: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    gelar_depan: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    nama_depan: Mapped[str] = mapped_column(String(100), nullable=True)  # Specify length
    nama_belakang: Mapped[str] = mapped_column(String(100), nullable=True)  # Specify length
    gelar_belakang: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    alamat: Mapped[str] = mapped_column(String(255), nullable=True)  # Specify length
    agama: Mapped[str] = mapped_column(String(50), nullable=True)  # Specify length
    telp_seluler: Mapped[str] = mapped_column(String(20), nullable=True) 
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    kelas: Mapped[List["Kelas"]] = relationship("Kelas", back_populates="dosen", lazy="selectin")
    pengajaran: Mapped[List["Pengajaran"]] = relationship("Pengajaran", back_populates="dosen", lazy="selectin")
    preferensi_jadwal_dosen: Mapped[List["PreferensiJadwalDosen"]] = relationship("PreferensiJadwalDosen", back_populates="dosen", lazy="selectin")
    
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="dosen", lazy="selectin")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True) 
    
from model.kelas_model import Kelas
from .pengajaran_model import Pengajaran 
from .preferensi_jadwal_dosen_model import PreferensiJadwalDosen
from .user_model import User

@event.listens_for(Dosen, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()