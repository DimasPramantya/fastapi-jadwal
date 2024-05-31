from fastapi import APIRouter, Depends, HTTPException, Query

from schemas.dosen_schema import CreateDosen, Dosen as DosenSchema, dosen_model_to_dict
from util.db_connection import AsyncSession, get_async_session
from controller.jadwal_controller import *
from schemas.pagination_schema import Page

router = APIRouter()

@router.get("",)
async def get_dosen_by_id(session: AsyncSession = Depends(get_async_session)):
    await generateJadwal(session)
    return {"message": f"Dosen with id  deleted successfully"}