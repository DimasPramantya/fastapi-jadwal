from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from schemas.pengajaran_schema import Pengajaran as PengajaranSchema, PengajaranCreate, PengajaranUpdate
from model.pengajaran_model import Pengajaran as PengajaranModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def getPengajaranById(
    id: int,
    session: AsyncSession
):
    pengajaran = await session.get(PengajaranModel, id)
    if not pengajaran:
        raise EntityNotFoundException("Pengajaran", id)
    return pengajaran

async def deletePengajaran(
    id: int,
    session: AsyncSession
):
    pengajaran = await session.get(PengajaranModel, id)
    if not pengajaran:
        raise EntityNotFoundException("Pengajaran", id)
    await session.delete(pengajaran)
    await session.commit()
    return

async def updatePengajaran(
    id: int,
    pengajaran: PengajaranUpdate,
    session: AsyncSession
):
    currentPengajaran = await session.get(PengajaranModel, id)
    if not currentPengajaran:
        raise EntityNotFoundException("Pengajaran", id)
    currentPengajaran.id_dosen = pengajaran.id_dosen
    currentPengajaran.id_kelas = pengajaran.id_kelas
    currentPengajaran.id_semester = pengajaran.id_semester
    currentPengajaran.id_mata_kuliah = pengajaran.id_mata_kuliah
    session.add(currentPengajaran)
    await session.commit()
    await session.refresh(currentPengajaran)
    return currentPengajaran

async def getPengajaranPageable(
    session: AsyncSession, skip: int = 0, limit: int = 10   
)->List[PengajaranModel]:
    result = await session.execute(
        select(PengajaranModel).limit(limit).offset(skip)
    )
    pengajaran_list = result.scalars().all()
    return pengajaran_list

async def getPengajaranCount(session: AsyncSession):
    result = await session.execute(select(func.count(PengajaranModel.id)))
    return result.scalar_one()
    