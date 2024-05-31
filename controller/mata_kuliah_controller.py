from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from schemas.mata_kuliah_schema import MataKuliah as MataKuliahSchema, MataKuliahCreate, MataKuliahUpdate
from model.mata_kuliah_model import MataKuliah as MataKuliahModel
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def getMataKuliahById(
    id: int,
    session: AsyncSession
) -> MataKuliahModel:
    mataKuliah = await session.get(MataKuliahModel, id)
    if not mataKuliah:
        raise EntityNotFoundException("Mata Kuliah", id)
    return mataKuliah

async def deleteMataKuliah(
    id: int,
    session: AsyncSession
):
    mataKuliah = await session.get(MataKuliahModel, id)
    await session.delete(mataKuliah)
    await session.commit()
    return

async def createMataKuliah(
    mataKuliah: MataKuliahCreate,
    session: AsyncSession
) -> MataKuliahModel:
    newMataKuliah = MataKuliahModel(
        nama_mata_kuliah= mataKuliah.nama_mata_kuliah,
        nama_mata_kuliah_inggris= mataKuliah.nama_mata_kuliah_inggris,
        is_lab= mataKuliah.is_lab,
        id_program_studi= mataKuliah.id_program_studi,
        nama_prodi= mataKuliah.nama_prodi,
        nama_prodi_en= mataKuliah.nama_prodi_en,
        index_minimum= mataKuliah.index_minimum,
        kd_mata_kuliah= mataKuliah.kd_mata_kuliah,
        semester= mataKuliah.semester,
        sks= mataKuliah.sks,
        tingkat_mata_kuliah= mataKuliah.tingkat_mata_kuliah,
        created_at= mataKuliah.created_at,
        updated_at= mataKuliah.updated_at,
    )
    session.add(newMataKuliah)
    await session.commit()
    await session.refresh(newMataKuliah)
    return newMataKuliah

async def getMataKuliahPageable(
    session: AsyncSession, skip: int = 0, limit: int = 10
) -> List[MataKuliahModel]:
    result = await session.execute(
        select(MataKuliahModel).limit(limit).offset(skip)
    )
    mata_kuliah_list = result.scalars().all()
    return mata_kuliah_list

async def updateMataKuliah(
    id: int, mataKuliah: MataKuliahUpdate, session: AsyncSession
) -> MataKuliahModel:
    currentMataKuliah = await session.get(MataKuliahModel, id)
    
    if not currentMataKuliah:
        raise EntityNotFoundException("Mata Kuliah", id)
    
    currentMataKuliah.id_program_studi = mataKuliah.id_program_studi
    currentMataKuliah.index_minimum = mataKuliah.index_minimum
    currentMataKuliah.is_lab = mataKuliah.is_lab
    currentMataKuliah.kd_mata_kuliah = mataKuliah.kd_mata_kuliah
    currentMataKuliah.nama_mata_kuliah = mataKuliah.nama_mata_kuliah
    currentMataKuliah.nama_mata_kuliah_inggris = mataKuliah.nama_mata_kuliah_inggris
    currentMataKuliah.nama_prodi = mataKuliah.nama_prodi
    currentMataKuliah.nama_prodi_en = mataKuliah.nama_prodi_en
    currentMataKuliah.semester = mataKuliah.semester
    currentMataKuliah.sks = mataKuliah.sks
    currentMataKuliah.tingkat_mata_kuliah = mataKuliah.tingkat_mata_kuliah
    
    session.add(currentMataKuliah)
    await session.commit()
    await session.refresh(currentMataKuliah)
    return currentMataKuliah

async def getMataKuliahCount(session: AsyncSession):
    result = await session.execute(select(func.count(MataKuliahModel.id)))
    return result.scalar_one()
