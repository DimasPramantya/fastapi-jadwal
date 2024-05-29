from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.kelas_schema import KelasCreate, KelasUpdate, Kelas as KelasSchema, kelas_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.kelas_controller import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.post("", response_model=KelasSchema)
async def create_new_kelas(kelas: KelasCreate, session: AsyncSession = Depends(get_async_session)):
    newKelas = await createNewKelas(kelas, session)
    if not newKelas:
        raise BadRequestException()
    return newKelas

@router.get("{id}", response_model=KelasSchema)
async def find_kelas_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    kelas = await getKelasById(id, session)
    return kelas

@router.get("", response_model=Page[KelasSchema])
async def find_kelas_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    kelas_list = await getKelasPageable(session, skip=offset, limit=limit)
    total = await getKelasCount(session)
    kelas_dict = [kelas_model_to_dict(d) for d in kelas_list]
    return Page(total_elements=total, items=kelas_dict, size=limit, page=skip)

@router.delete("/{id}")
async def delete_kelas_by_id(
    id: int, 
    session = Depends(get_async_session)
):
    await deleteKelas(id, session)
    return {"message": f"Kelas with id {id} deleted successfully"}

@router.put("/{id}", response_model=KelasSchema)
async def update_kelas(
    id: int,
    kelas: KelasUpdate,
    session = Depends(get_async_session)
):
    return await updateKelas(id, kelas, session)
    