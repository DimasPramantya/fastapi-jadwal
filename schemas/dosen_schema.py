#/schemas/dosen_schema.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .preferensi_jadwal_dosen_schema import preferensi_jadwal_dosen_model_to_dict, PreferensiJadwalDosen

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
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    preferensi: List[PreferensiJadwalDosen] = []
    
class CreateDosen(DosenBase):
    pass

class UpdateDosen(DosenBase):
    pass

class Dosen(DosenBase):
    id: int
    
    class Config:
        orm_mode = True

def dosen_model_to_dict(dosen: Dosen):
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
        "email": dosen.email,
        "preferensi": [preferensi_jadwal_dosen_model_to_dict(p) for p in dosen.preferensi_jadwal_dosen] if dosen.preferensi_jadwal_dosen else None,  
        "created_at": dosen.created_at,
        "updated_at": dosen.updated_at
    }