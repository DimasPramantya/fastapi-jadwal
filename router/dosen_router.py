from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.dosen_schema import CreateDosen, Dosen as DosenSchema, dosen_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.dosen_controller import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.post("", response_model=DosenSchema)
async def create_new_dosen(dosen: CreateDosen, session: AsyncSession = Depends(get_async_session)):
    new_dosen = await createDosen(dosen, session)
    if not new_dosen:
        raise HTTPException(status_code=400, detail="Dosen could not be created")
    return new_dosen


@router.delete("/{id}")
async def delete_dosen_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    deleted = await deleteDosen(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Dosen with id {id} not found")
    return {"message": f"Dosen with id {id} deleted successfully"}

@router.get("/{id}", response_model=DosenSchema)
async def get_dosen_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    dosen = await getDosenById(id, session)
    return dosen


@router.get("", response_model=Page[DosenSchema])
async def get_dosen_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    dosen_list = await getDosenPageable(session, skip=offset, limit=limit)
    total = await getDosenCount(session)
    items_dict = [dosen_model_to_dict(d) for d in dosen_list]
    return Page(total_elements=total, items=items_dict, size=limit, page=skip)
        
@router.put("{id}", response_model=DosenSchema)
async def update_dosen(
    id: int,
    dosen: UpdateDosen,
    session = Depends(get_async_session)
):
    return await updateDosen(id, dosen, session)
