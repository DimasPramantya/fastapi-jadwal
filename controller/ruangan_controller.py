from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from model.ruangan_model import Ruangan as RuanganModel
from schemas.ruangan_schema import Ruangan as RuanganSchema, RuanganCreate, RuanganUpdate
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def createNewRuangan(
    ruangan: RuanganCreate, 
    session: AsyncSession
) -> RuanganModel:
    newRuangan = RuanganModel(
        nama_ruangan = ruangan.nama_ruangan,
        nama_gedung = ruangan.nama_gedung,
        is_lab = ruangan.is_lab,
        kapasitas = ruangan.kapasitas
    )
    session.add(newRuangan)
    await session.commit()
    await session.refresh(newRuangan)
    return newRuangan

async def deleteRuangan(
    id: int, 
    session: AsyncSession
):
    ruangan = await session.get(RuanganModel, id)
    if not ruangan:
        raise EntityNotFoundException("Ruangan", id)
    await session.delete(ruangan)
    await session.commit()
    return

async def updateRuangan(
    id: int,
    ruangan: RuanganUpdate,
    session: AsyncSession
) -> RuanganModel:
    current_ruangan = await session.get(RuanganModel, id)
    if not current_ruangan:
        raise EntityNotFoundException("ruangan", id)
    
    current_ruangan.is_lab = ruangan.is_lab
    current_ruangan.kapasitas = ruangan.kapasitas
    current_ruangan.nama_gedung = ruangan.nama_gedung
    current_ruangan.nama_ruangan = ruangan.nama_ruangan

    session.add(current_ruangan)
    await session.commit()
    await session.refresh(current_ruangan)

    return current_ruangan

async def getRuanganById(
    id: int,
    session: AsyncSession
) -> RuanganModel:
    ruangan = await session.get(RuanganModel, id)
    if not ruangan:
        raise EntityNotFoundException("Ruangan", id)
    return ruangan

async def getRuanganPageable(
    session: AsyncSession, skip: int = 0, limit: int = 10
)-> List[RuanganModel]:
    result = await session.execute(
        select(RuanganModel).limit(limit).offset(skip)
    )
    ruangan_list = result.scalars().all()
    return ruangan_list

async def getRuanganCount(session: AsyncSession):
    result = await session.execute(select(func.count(RuanganModel.id)))
    return result.scalar_one()
