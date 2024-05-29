from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List
from sqlalchemy import String, ForeignKey, DateTime, event
from datetime import datetime

from . import Base

class PreferensiJadwalDosen(Base):
    __tablename__ = "preferensi_jadwal_dosen"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    id_dosen: Mapped[int] = mapped_column(ForeignKey("dosen.id"))
    dosen: Mapped["Dosen"] = relationship("Dosen", back_populates="preferensi_jadwal_dosen", lazy="selectin")

    id_slot: Mapped[int] = mapped_column(ForeignKey("slot.id"))
    slot: Mapped["Slot"] = relationship("Slot", back_populates="preferensi_jadwal_dosen", lazy="selectin")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)



from .dosen_model import Dosen
from .slot_model import Slot

@event.listens_for(PreferensiJadwalDosen, 'before_update')
def update_timestamp(mapper, connection, target):
    target.updated_at = datetime.now()