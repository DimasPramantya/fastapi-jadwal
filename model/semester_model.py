from datetime import date, datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, Date, ForeignKey, DateTime, event
from typing import List

from . import Base

class Semester(Base):
    __tablename__ = "semester"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    jenis: Mapped[str] = mapped_column(String(30))
    tahun_ajaran: Mapped[str] = mapped_column(String(30))
    tanggal_mulai: Mapped[date] = mapped_column(Date)
    tanggal_berakhir: Mapped[date] = mapped_column(Date)
    pengajaran: Mapped[List["Pengajaran"]] = relationship("Pengajaran", back_populates="semester", lazy="selectin")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

from .pengajaran_model import Pengajaran

@event.listens_for(Semester, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()