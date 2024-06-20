from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy import String, ForeignKey, DateTime
from datetime import datetime

from . import Base

class Pengajaran(Base):
    __tablename__ = "pengajaran"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    id_kelas: Mapped[int] = mapped_column(ForeignKey("kelas.id"))
    kelas: Mapped["Kelas"] = relationship("Kelas",back_populates="pengajaran", lazy="selectin")
    
    id_dosen: Mapped[int] = mapped_column(ForeignKey("dosen.id"))
    dosen: Mapped["Dosen"] = relationship("Dosen", back_populates="pengajaran", lazy="selectin")
    
    id_mata_kuliah: Mapped[int] = mapped_column(ForeignKey("mata_kuliah.id"))
    mata_kuliah: Mapped["MataKuliah"] = relationship("MataKuliah", back_populates="pengajaran", lazy="selectin")

    id_semester: Mapped[int] = mapped_column(ForeignKey("semester.id"))
    semester: Mapped["Semester"] = relationship("Semester", back_populates="pengajaran", lazy="selectin")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    jadwal: Mapped[List["Jadwal"]] = relationship("Jadwal", back_populates="pengajaran", lazy="selectin")
    jadwal_sementara: Mapped[List["JadwalSementara"]] = relationship("JadwalSementara", back_populates="pengajaran", lazy="selectin")


from .dosen_model import Dosen
from .mata_kuliah_model import MataKuliah
from .kelas_model import Kelas
from .jadwal_model import Jadwal
from .semester_model import Semester
from .jadwal_sementara import JadwalSementara
    