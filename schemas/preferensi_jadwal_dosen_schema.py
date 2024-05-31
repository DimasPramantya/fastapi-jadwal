from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .slot_schema import Slot, slot_model_to_dict
from .dosen_schema import Dosen, dosen_model_to_dict

class PreferensiJadwalDosenBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class PreferensiJadwalDosenCreate(PreferensiJadwalDosenBase):
    id_dosen: Optional[int] = None
    id_slot: Optional[int] = None

class PreferensiJadwalDosenUpdate(PreferensiJadwalDosenBase):
    id_dosen: Optional[int]
    id_slot: Optional[int] 

class PreferensiJadwalDosen(PreferensiJadwalDosenBase):
    id: int
    id_dosen: Optional[int]
    id_slot: Optional[int]
    dosen: Optional[Dosen]
    slot: Optional[Slot]

    class Config:
        orm_mode = True
        from_attributes = True

def preferensi_jadwal_dosen_model_to_dict(e: PreferensiJadwalDosen):
    return {
        "id": e.id,
        "created_at": e.created_at,
        "updated_at": e.updated_at,
        "dosen": None if e.dosen is None else dosen_model_to_dict(e.dosen),
        "slot": None if e.slot is None else slot_model_to_dict(e.slot),
    }