from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.preferensi_jadwal_dosen_schema import PreferensiJadwalDosen as PreferensiJadwalDosenSchema, PreferensiJadwalDosenCreate, PreferensiJadwalDosenUpdate, preferensi_jadwal_dosen_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.preferensi_jadwal_dosen import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.get("{id}", response_model=PreferensiJadwalDosenSchema)
async def get_preferensi_jadwal_dosen_by_id(
    id: int,
    session = Depends(get_async_session)
)->PreferensiJadwalDosenSchema:
    return await getById(id, session)

@router.get("", response_model=Page[PreferensiJadwalDosenSchema])
async def get_preferensi_jadwal_dosen_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session) 
)-> Page[PreferensiJadwalDosenSchema]:
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    preferensiJadwalDosenList = await getPreferensiJadwalDosenPageable(session, offset, limit)
    total = await getPreferensiJadwalDosenCount(session)
    preferensiJadwalDosenDict = [preferensi_jadwal_dosen_model_to_dict(d) for d in preferensiJadwalDosenList]
    return Page(total_elements=total, items=preferensiJadwalDosenDict, size=limit, page=skip)

@router.delete("{id}")
async def delete_preferensi_jadwal_dosen(
    id: int,
    session = Depends(get_async_session)
):
    await deletePreferensiJadwalDosen(id, session)
    return {"message": f"Preferensi Jadwal Dosen with id {id} deleted successfully"}

@router.put("{id}", response_model=PreferensiJadwalDosenSchema)
async def update_preferensi_jadwal_dosen(
    id: int,
    preferensiJadwalDosen: PreferensiJadwalDosenUpdate,
    session = Depends(get_async_session)
)->PreferensiJadwalDosenSchema:
    return await updatePreferensiJadwalDosen(id, preferensiJadwalDosen, session)

@router.post("", response_model=PreferensiJadwalDosenSchema)
async def add_preferensi_jadwal_dosen(
    preferensiJadwalDosen: PreferensiJadwalDosenCreate,
    session = Depends(get_async_session)
)->PreferensiJadwalDosenSchema:
    return await postPreferensiJadwalDosen(preferensiJadwalDosen, session)