#/schemas/dosen_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BaseModel(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

class DosenBase(BaseModel):
    __tablename__ = "dosen"

    nip: str
    nidn: str
    id_pegawai: str
    inisial: str
    gelar_depan: str
    nama_depan: str
    nama_belakang: str
    gelar_belakang: str
    alamat: str
    agama: str
    telp_seluler: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
class CreateDosen(DosenBase):
    pass

class UpdateDosen(DosenBase):
    pass

class Dosen(DosenBase):
    id: int
    
    class Config:
        orm_mode = True

def dosen_model_to_dict(dosen):
    return {
        "id": dosen.id,
        "nip": dosen.nip,
        "nidn": dosen.nidn,
        "id_pegawai": dosen.id_pegawai,
        "inisial": dosen.inisial,
        "gelar_depan": dosen.gelar_depan,
        "nama_depan": dosen.nama_depan,
        "nama_belakang": dosen.nama_belakang,
        "gelar_belakang": dosen.gelar_belakang,
        "alamat": dosen.alamat,
        "agama": dosen.agama,
        "telp_seluler": dosen.telp_seluler,
        "created_at": dosen.created_at,
        "updated_at": dosen.updated_at
    }