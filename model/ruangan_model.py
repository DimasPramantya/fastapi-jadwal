from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, DateTime, event
from datetime import datetime
from typing import List

from . import Base

class Ruangan(Base):
    __tablename__ = "ruangan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nama_ruangan: Mapped[str] = mapped_column(String(5), nullable=True)
    nama_gedung: Mapped[str] = mapped_column(String(25), nullable=True)
    kapasitas: Mapped[int] = mapped_column(nullable=True)
    is_lab: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    jadwal: Mapped[List["Jadwal"]] = relationship("Jadwal", back_populates="ruangan", lazy="selectin")
    jadwal_sementara: Mapped[List["JadwalSementara"]] = relationship("JadwalSementara", back_populates="ruangan", lazy="selectin")

from .jadwal_model import Jadwal
from .jadwal_sementara import JadwalSementara

@event.listens_for(Ruangan, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()