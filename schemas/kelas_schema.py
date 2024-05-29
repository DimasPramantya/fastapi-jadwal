from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .dosen_schema import Dosen, dosen_model_to_dict

class KelasBase(BaseModel):
    nama_kelas: str
    id_prodi: int
    nama_prodi: str
    shift: str
    kuota: int 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class KelasCreate(KelasBase):
    id_dosen_wali: Optional[int] = None 

class KelasUpdate(KelasBase):
    id_dosen_wali: Optional[int]


class Kelas(KelasBase):
    id: int
    id_dosen_wali: Optional[int]
    dosen: Optional[Dosen]

    class Config:
        orm_mode = True
        from_attributes = True

def kelas_model_to_dict(kelas: Kelas):
    return {
        "id": kelas.id,
        "nama_kelas": kelas.nama_kelas,
        "id_prodi": kelas.id_prodi,
        "nama_prodi": kelas.nama_prodi,
        "shift": kelas.shift,
        "kuota": kelas.kuota,
        "id_dosen_wali": None if kelas.id_dosen_wali is None else kelas.id_dosen_wali,
        "created_at": kelas.created_at,
        "updated_at": kelas.updated_at,
        "dosen": None if kelas.dosen is None else dosen_model_to_dict(kelas.dosen)
    }