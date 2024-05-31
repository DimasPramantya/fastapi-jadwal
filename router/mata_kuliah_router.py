from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.pagination_schema import Page
from util.db_connection import AsyncSession, get_async_session
from controller.mata_kuliah_controller import *
from schemas.mata_kuliah_schema import MataKuliah as MataKuliahSchema, MataKuliahCreate, MataKuliahUpdate, mata_kuliah_model_to_dict

router = APIRouter()

@router.post("", response_model=MataKuliahSchema)
async def add_mata_kuliah(
    mataKuliah: MataKuliahCreate,
    session: AsyncSession = Depends(get_async_session)
):
    return await createMataKuliah(mataKuliah, session)

@router.get("{id}", response_model=MataKuliahSchema)
async def find_mata_kuliah_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session)
): 
    return await getMataKuliahById(id, session)

@router.get("", response_model=Page[MataKuliahSchema])
async def get_mata_kuliah_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    mataKuliahList = await getMataKuliahPageable(session, skip=offset, limit=limit)
    total = await getMataKuliahCount(session)
    mataKuliahDict = [mata_kuliah_model_to_dict(d) for d in mataKuliahList]
    return Page(total_elements=total, items=mataKuliahDict, size=limit, page=skip)

@router.delete("{id}")
async def delete_mata_kuliah(
    id: int,
    session = Depends(get_async_session)
): 
    await deleteMataKuliah(id, session)
    return {"message": f"Mata Kuliah with id {id} deleted successfully"}

@router.put("{id}")
async def update_mata_kuliah(
    id: int,
    session = Depends(get_async_session)
):
    return await updateMataKuliah(id, session)