from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from schemas.preferensi_jadwal_dosen_schema import PreferensiJadwalDosen as PreferensiJadwalDosenSchema, PreferensiJadwalDosenCreate, PreferensiJadwalDosenUpdate
from model.preferensi_jadwal_dosen_model import PreferensiJadwalDosen as PreferensiJadwalDosenModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def getById(
    id: int,
    session: AsyncSession
):
    current_entity = await session.get(PreferensiJadwalDosenModel.id)
    if not current_entity:
        raise EntityNotFoundException("Preferensi Jadwal Dosen", id)
    return current_entity

async def postPreferensiJadwalDosen(
    preferensiJadwalDosen: PreferensiJadwalDosenCreate,
    session: AsyncSession
):
    newEntity = PreferensiJadwalDosenModel(
        id_dosen = preferensiJadwalDosen.id_dosen,
        id_slot = preferensiJadwalDosen.id_slot,
    )
    session.add(newEntity)
    await session.commit()
    await session.refresh(newEntity)
    return newEntity

async def updatePreferensiJadwalDosen(
    id: int,
    preferensiJadwalDosen: PreferensiJadwalDosenUpdate,
    session: AsyncSession
):
    entity = await session.get(PreferensiJadwalDosenModel, id)
    if not entity:
        raise EntityNotFoundException("PreferensiJadwalDosen", id)
    entity.id_dosen = preferensiJadwalDosen.id_dosen
    entity.id_slot = preferensiJadwalDosen.id_slot
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity

async def deletePreferensiJadwalDosen(
    id: int,
    session: AsyncSession
):
    entity = await session.get(PreferensiJadwalDosenModel, id)
    if not entity:
        raise EntityNotFoundException("PreferensiJadwalDosen", id)
    await session.delete(entity)
    await session.commit()
    return

async def getPreferensiJadwalDosenPageable(
    session: AsyncSession, skip: int = 0, limit: int = 10  
)-> List[PreferensiJadwalDosenModel]:
    result = await session.execute(
        select(PreferensiJadwalDosenModel).limit(limit).offset(skip)
    )
    entity_list = result.scalars().all()
    return entity_list

async def getPreferensiJadwalDosenCount(session: AsyncSession):
    result = await session.execute(select(func.count(PreferensiJadwalDosenModel.id)))
    return result.scalar_one()
