# controller/dosen_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from schemas.dosen_schema import CreateDosen, Dosen as DosenSchema, UpdateDosen
from model.dosen_model import Dosen as DosenModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def createDosen(dosen: CreateDosen, session: AsyncSession) -> DosenModel:
    new_dosen = DosenModel(
        nip=dosen.nip,
        nidn=dosen.nidn,
        id_pegawai=dosen.id_pegawai,
        inisial=dosen.inisial,
        gelar_depan=dosen.gelar_depan,
        nama_depan=dosen.nama_depan,
        nama_belakang=dosen.nama_belakang,
        gelar_belakang=dosen.gelar_belakang,
        alamat=dosen.alamat,
        agama=dosen.agama,
        telp_seluler=dosen.telp_seluler,
        email=dosen.email
    )
    session.add(new_dosen)
    await session.commit()
    await session.refresh(new_dosen)
    return new_dosen

async def deleteDosen(id: int, session: AsyncSession):
    dosen = await session.get(DosenModel, id)
    if not dosen:
        raise EntityNotFoundException(entity_name="Dosen", entity_id=id)
    await session.delete(dosen)
    await session.commit()
    return True

async def getDosenById(id: int, session: AsyncSession) -> DosenModel:
    result = await session.execute(select(DosenModel).where(DosenModel.id == id))
    dosen = result.scalar_one_or_none()
    if not dosen:
        raise EntityNotFoundException(entity_name="Dosen", entity_id=id)
    return dosen

async def getDosenPageable(session: AsyncSession, skip: int = 0, limit: int = 10) -> List[DosenModel]:
    result = await session.execute(
        select(DosenModel).offset(skip).limit(limit)
    )
    dosen_list = result.scalars().all()
    return dosen_list

async def getDosenCount(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(DosenModel.id)))
    count = result.scalar_one()
    return count

async def updateDosen(id: int, dosen: UpdateDosen, session:AsyncSession) -> DosenModel:
    currentDosen = await session.get(DosenModel, id)
    if not currentDosen:
        raise EntityNotFoundException(entity_name="Dosen", entity_id=id)
    
    currentDosen.agama = dosen.agama
    currentDosen.alamat = dosen.alamat
    currentDosen.gelar_belakang = dosen.gelar_belakang
    currentDosen.gelar_depan = dosen.gelar_depan
    currentDosen.id_pegawai = dosen.id_pegawai
    currentDosen.inisial = dosen.inisial
    currentDosen.nama_depan = dosen.nama_depan
    currentDosen.nama_belakang = dosen.nama_belakang
    currentDosen.nidn = dosen.nidn
    currentDosen.nip = dosen.nip
    currentDosen.telp_seluler = dosen.telp_seluler
    
    session.add(currentDosen)
    await session.commit()
    await session.refresh(currentDosen)
    return currentDosen

