from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class MataKuliahBase(BaseModel):
    kd_mata_kuliah: str
    nama_mata_kuliah: str
    nama_mata_kuliah_inggris: str
    sks: int
    semester: str
    tingkat_mata_kuliah: int
    is_lab: bool
    index_minimum: bool
    id_program_studi: int
    nama_prodi: str
    nama_prodi_en: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class MataKuliahCreate(MataKuliahBase):
    pass

class MataKuliahUpdate(MataKuliahBase):
    pass


class MataKuliah(MataKuliahBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

def mata_kuliah_model_to_dict(mataKuliah: MataKuliah):
    return {
        "id": mataKuliah.id,
        "nama_mata_kuliah": mataKuliah.nama_mata_kuliah,
        "nama_mata_kuliah_inggris": mataKuliah.nama_mata_kuliah_inggris,
        "is_lab": mataKuliah.is_lab,
        "id_program_studi": mataKuliah.id_program_studi,
        "nama_prodi": mataKuliah.nama_prodi,
        "nama_prodi_end": mataKuliah.nama_prodi_en,
        "index_minimum": mataKuliah.index_minimum,
        "kd_mata_kuliah": mataKuliah.kd_mata_kuliah,
        "semester": mataKuliah.semester,
        "sks": mataKuliah.sks,
        "tingkat_mata_kuliah": mataKuliah.tingkat_mata_kuliah,
        "created_at": mataKuliah.created_at,
        "updated_at": mataKuliah.updated_at,
    }