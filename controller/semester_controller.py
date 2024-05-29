from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from model.semester_model import Semester as SemesterModel
from schemas.semester_schema import Semester as SemesterSchema, SemesterCreate, SemesterUpdate
from exceptions.entity_not_found_exception import EntityNotFoundException
from exceptions.bad_request_exception import BadRequestException

async def getSemesterById(id: int, session: AsyncSession) -> SemesterModel:
    semester = await session.get(SemesterModel, id)
    if not semester:
        raise EntityNotFoundException("Semester", id)
    return semester

async def createNewSemester(semester: SemesterCreate, session: AsyncSession) -> SemesterModel:
    newSemester = SemesterModel(
        jenis = semester.jenis,
        tahun_ajaran = semester.tahun_ajaran,
        tanggal_mulai = semester.tanggal_mulai,
        tanggal_berakhir = semester.tanggal_berakhir
    )
    session.add(newSemester)
    await session.commit()
    await session.refresh(newSemester)
    return newSemester

async def updateSemester(id: int, semester: SemesterUpdate, session: AsyncSession) -> SemesterModel:
    currentSemester = await session.get(SemesterModel, id)
    if not currentSemester:
        raise EntityNotFoundException("semester", id)
    
    currentSemester.jenis = semester.jenis
    currentSemester.tahun_ajaran = semester.tahun_ajaran
    currentSemester.tanggal_mulai = semester.tanggal_mulai
    currentSemester.tanggal_berakhir = semester.tanggal_berakhir
    
    session.add(currentSemester)
    await session.commit()
    await session.refresh(currentSemester)

    return currentSemester

async def deleteSemesterById(id: int, session: AsyncSession):
    semester = await session.get(SemesterModel, id)
    await session.delete(semester)
    await session.commit()
    return

async def getSemesterPageable(
    session: AsyncSession,
    skip: int = 0, 
    limit: int = 10,
):
    result = await session.execute(
        select(SemesterModel).offset(skip).limit(limit)
    )
    semester_list = result.scalars().all()
    return semester_list

async def getSemesterCount(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(SemesterModel.id)))
    return result.scalar_one()