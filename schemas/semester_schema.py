from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

class SemesterBase(BaseModel):
    jenis: str
    tahun_ajaran: str
    tanggal_mulai: date
    tanggal_berakhir: date
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class SemesterCreate(SemesterBase):
    pass

class SemesterUpdate(SemesterBase):
    pass

class Semester(SemesterBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

def semester_model_to_dict(semester: Semester):
    return {
        "id": semester.id, 
        "jenis": semester.jenis,
        "tahun_ajaran": semester.tahun_ajaran,
        "tanggal_mulai": semester.tanggal_mulai,
        "tanggal_berakhir": semester.tanggal_berakhir,
        "created_at": semester.created_at,
        "updated_at": semester.updated_at,
    }