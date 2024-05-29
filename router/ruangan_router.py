from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.ruangan_schema import RuanganCreate, RuanganUpdate, Ruangan as RuanganSchema, ruangan_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.ruangan_controller import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.get("", response_model=Page[RuanganSchema])
async def get_ruangan_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    ruanganList = await getRuanganPageable(session, offset, limit)
    total = await getRuanganCount(session)
    ruanganDict = [ruangan_model_to_dict(d) for d in ruanganList]
    return Page(total_elements=total, items=ruanganDict, size=limit, page=skip)

@router.get("{id}", response_model=RuanganSchema)
async def get_ruangan_by_id(
    id: int,
    session = Depends(get_async_session)
):
    return await getRuanganById(id, session)

@router.put("{id}", response_model=RuanganSchema)
async def edit_ruangan(
    id: int,
    ruangan: RuanganUpdate,
    session = Depends(get_async_session)
):
    return await updateRuangan(id, ruangan, session)

@router.delete("{id}")
async def delete_ruangan(
    id: int,
    session = Depends(get_async_session)
):
    await deleteRuangan(id, session)
    return {"message": f"Ruangan with id {id} deleted successfully"}

@router.post("", response_model=RuanganSchema)
async def add_ruangan(
    ruangan: RuanganCreate,
    session = Depends(get_async_session)
):
    return await createNewRuangan(ruangan, session)
