from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.jadwal_sementara_schema import jadwal_sementara_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.jadwal_controller import *
from schemas.pagination_schema import Page
from fastapi.security import HTTPBearer
from typing import Annotated

security = HTTPBearer()

async def get_token(token: str = Depends(security)):
    return token

router = APIRouter()

@router.post("/temp")
async def generate_jadwal_sementara(session: AsyncSession = Depends(get_async_session)):
    best_violating_preferences, conflict_list = await generateJadwalSementara(session)
    return {"best_violating_preferences": best_violating_preferences, "conflict_list": conflict_list}

@router.get("/temp")
async def get_jadwal_sementara_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    jadwal_list = await getJadwalSementaraPageable(session, skip=offset, limit=limit)
    total = await getJadwalSementaraCount(session)
    items_dict = [jadwal_sementara_to_dict(d) for d in jadwal_list]
    return Page(total_elements=total, items=items_dict, size=limit, page=skip)

@router.post("/")
async def generate_all_jadwal(
    credentials: str = Depends(get_token),
    session = Depends(get_async_session)
):
    print(credentials)
    await generateJadwal(credentials.credentials, session)
    return