from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

class RuanganBase(BaseModel):
    nama_ruangan: str
    nama_gedung: str
    kapasitas: int
    is_lab: Optional[bool]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class RuanganCreate(RuanganBase):
    pass

class RuanganUpdate(RuanganBase):
    pass

class Ruangan(RuanganBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

def ruangan_model_to_dict(ruangan: Ruangan):
    return {
        "nama_ruangan": ruangan.nama_ruangan,
        "nama_gedung": ruangan.nama_gedung,
        "kapasitas": ruangan.kapasitas,
        "is_lab": ruangan.is_lab,
        "created_at": ruangan.created_at,
        "updated_at": ruangan.updated_at
    }