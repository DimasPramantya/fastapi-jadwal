from datetime import datetime, time
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy import String, DateTime, Boolean, Time

from . import Base

class Slot(Base):
    __tablename__ = "slot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    is_lab_slot: Mapped[bool] = mapped_column(Boolean)
    day: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    preferensi_jadwal_dosen: Mapped[List["PreferensiJadwalDosen"]] = relationship("PreferensiJadwalDosen", back_populates="slot", lazy="selectin")
    jadwal: Mapped[List["Jadwal"]] = relationship("Jadwal", back_populates="slot", lazy="selectin")
    jadwal_sementara: Mapped[List["JadwalSementara"]] = relationship("JadwalSementara", back_populates="slot", lazy="selectin")

from .jadwal_model import Jadwal
from .jadwal_sementara import JadwalSementara
from .preferensi_jadwal_dosen_model import PreferensiJadwalDosen
