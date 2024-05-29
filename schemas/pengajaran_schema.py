from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .kelas_schema import Kelas, kelas_model_to_dict
from .mata_kuliah_schema import MataKuliah, mata_kuliah_model_to_dict
from .semester_schema import Semester, semester_model_to_dict
from .dosen_schema import Dosen, dosen_model_to_dict

class PengajaranBase(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class PengajaranCreate(PengajaranBase):
    id_dosen: Optional[int] = None
    id_kelas: Optional[int] = None
    id_mata_kuliah: Optional[int] = None 
    id_semester: Optional[int] = None

class PengajaranUpdate(PengajaranBase):
    id_dosen: Optional[int]
    id_kelas: Optional[int] 
    id_mata_kuliah: Optional[int]
    id_semester: Optional[int]

class Pengajaran(PengajaranBase):
    id: int
    id_dosen: Optional[int]
    id_kelas: Optional[int]
    id_mata_kuliah: Optional[int]
    id_semester: Optional[int] 
    dosen: Optional[Dosen]
    kelas: Optional[Kelas]
    mata_kuliah: Optional[MataKuliah]
    semester: Optional[Semester]

    class Config:
        orm_mode = True
        from_attributes = True

def pengajaran_model_to_dict(pengajaran: Pengajaran):
    return {
        "id": pengajaran.id,
        "created_at": pengajaran.created_at,
        "updated_at": pengajaran.updated_at,
        "dosen": None if pengajaran.dosen is None else dosen_model_to_dict(pengajaran.dosen),
        "kelas": None if pengajaran.kelas is None else kelas_model_to_dict(pengajaran.kelas),
        "semester": None if pengajaran.semester is None else semester_model_to_dict(pengajaran.semester),
        "mata_kuliah": None if pengajaran.mata_kuliah is None else mata_kuliah_model_to_dict(pengajaran.mata_kuliah)
    }