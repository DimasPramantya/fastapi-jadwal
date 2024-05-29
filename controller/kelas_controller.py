from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from schemas.kelas_schema import KelasCreate, KelasUpdate, Kelas as KelasSchema, kelas_model_to_dict
from model.dosen_model import Dosen as DosenModel
from model.kelas_model import Kelas as KelasModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def getKelasById(id: int, session: AsyncSession) -> KelasModel:
    result = await session.execute(select(KelasModel).where(KelasModel.id == id))
    kelas = result.scalar_one_or_none()
    if not kelas:
        raise EntityNotFoundException(entity_name="Kelas", entity_id=id)
    return kelas

async def createNewKelas(kelas: KelasCreate, session: AsyncSession) -> KelasModel:
    newKelas = KelasModel(
        nama_kelas= kelas.nama_kelas,
        id_prodi= kelas.id_prodi,
        nama_prodi= kelas.nama_prodi,
        shift= kelas.shift,
        kuota= kelas.kuota,
    )
    if kelas.id_dosen_wali:
        dosen = await session.get(DosenModel, kelas.id_dosen_wali)
        newKelas.id_dosen_wali = dosen.id
    
    session.add(newKelas)
    await session.commit()
    await session.refresh(newKelas)
    return newKelas

async def getKelasPageable(session: AsyncSession, skip: int = 0, limit: int = 10) -> List[KelasModel]:
    result = await session.execute(
        select(KelasModel).limit(limit).offset(skip)
    )
    kelas_list = result.scalars().all()
    return kelas_list

async def getKelasCount(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(KelasModel.id)))
    return result.scalar_one()

async def deleteKelas(id: int, session: AsyncSession):
    kelas = await session.get(KelasModel, id)
    await session.delete(kelas)
    await session.commit()
    return

async def updateKelas(id: int, kelas: KelasUpdate, session: AsyncSession) -> KelasModel:
    currentKelas = await session.get(KelasModel, id)
    if not currentKelas:
        raise EntityNotFoundException(entity_name="Kelas", entity_id=id)

    currentKelas.nama_kelas = kelas.nama_kelas
    currentKelas.nama_prodi = kelas.nama_prodi
    currentKelas.kuota = kelas.kuota
    currentKelas.id_dosen_wali = kelas.id_dosen_wali
    currentKelas.id_prodi = kelas.id_prodi
    currentKelas.shift = kelas.shift
    
    dosen_wali = await session.get(DosenModel, kelas.id_dosen_wali)
    if not dosen_wali:
        raise EntityNotFoundException(entity_name="Dosen", entity_id=kelas.id_dosen_wali)
    
    currentKelas.id_dosen_wali = dosen_wali.id
    
    session.add(currentKelas)
    await session.commit()
    await session.refresh(currentKelas)
    return currentKelas
