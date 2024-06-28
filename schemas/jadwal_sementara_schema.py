from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .pengajaran_schema import pengajaran_model_to_dict, Pengajaran
from .slot_schema import slot_model_to_dict, Slot
from .ruangan_schema import ruangan_model_to_dict, Ruangan

class BaseModel(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

class JadwalSementaraBase(BaseModel):
    id_pengajaran: int
    id_slot: int
    id_ruangan: int
    is_conflicted: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class JadwalSementaraCreate(JadwalSementaraBase):
    pass

class JadwalSementaraUpdate(BaseModel):
    id_slot: int
    id_ruangan: int
    updated_at: datetime = Field(default_factory=datetime.now)

class JadwalSementara(JadwalSementaraBase):
    id: int
    pengajaran: Pengajaran
    slot: Slot
    ruangan: Ruangan

    class Config:
        orm_mode = True
        from_attributes = True

def jadwal_sementara_to_dict(jadwal: JadwalSementara):
    return{
        "id": jadwal.id,
        "id_slot": jadwal.id_slot,
        "id_ruangan": jadwal.id_ruangan,
        "id_pengajaran": jadwal.id_pengajaran,
        "is_conflicted": jadwal.is_conflicted,
        "slot": slot_model_to_dict(jadwal.slot),
        "ruangan": ruangan_model_to_dict(jadwal.ruangan),
        "pengajaran": pengajaran_model_to_dict(jadwal.pengajaran)
    }