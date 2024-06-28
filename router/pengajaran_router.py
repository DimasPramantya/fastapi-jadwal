from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.pengajaran_schema import Pengajaran as PengajaranSchema, PengajaranCreate, PengajaranUpdate, pengajaran_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.pengajaran_controller import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.get("/{id}", response_model=PengajaranSchema)
async def get_pengajaran_by_id(
    id: int,
    session = Depends(get_async_session)
)->PengajaranSchema:
    return await getPengajaranById(id, session)

@router.get("", response_model=Page[PengajaranSchema])
async def get_pengajaran_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session) 
)-> Page[PengajaranSchema]:
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    pengajaranList = await getPengajaranPageable(session, offset, limit)
    total = await getPengajaranCount(session)
    pengajaranDict = [pengajaran_model_to_dict(d) for d in pengajaranList]
    return Page(total_elements=total, items=pengajaranDict, size=limit, page=skip)

@router.delete("/{id}")
async def delete_pengajaran(
    id: int,
    session = Depends(get_async_session)
):
    await deletePengajaran(id, session)
    return {"message": f"Pengajaran with id {id} deleted successfully"}

@router.put("/{id}", response_model=PengajaranSchema)
async def update_pengajaran(
    id: int,
    pengajaran: PengajaranUpdate,
    session = Depends(get_async_session)
)->PengajaranSchema:
    return await updatePengajaran(id, pengajaran, session)

@router.post("", response_model=PengajaranSchema)
async def add_pengajaran(
    pengajaran: PengajaranCreate,
    session = Depends(get_async_session)
)->PengajaranSchema:
    return await addPengajaran(pengajaran, session)