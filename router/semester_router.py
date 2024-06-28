from fastapi import APIRouter, Depends, HTTPException, Query

from util.db_connection import AsyncSession, get_async_session
from schemas.pagination_schema import Page
from schemas.semester_schema import Semester as SemesterSchema, semester_model_to_dict
from controller.semester_controller import *

router = APIRouter()

@router.get("", response_model=Page[SemesterSchema])
async def get_semester_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
):
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    semesterList = await getSemesterPageable(session, offset, limit)
    total = await getSemesterCount(session)
    semesterDict = [semester_model_to_dict(d) for d in semesterList]
    return Page(total_elements=total, items=semesterDict, size=limit, page=skip)

@router.get("/{id}", response_model=SemesterSchema)
async def get_semester_by_id(
    id: int,
    session = Depends(get_async_session)
):
    return await getSemesterById(id, session)


@router.put("/{id}", response_model=SemesterSchema)
async def update_semester(
    id: int,
    semester: SemesterUpdate,
    session = Depends(get_async_session)
):
    return await updateSemester(id, semester, session)

@router.post("", response_model=SemesterSchema)
async def create_new_semester(
    semester: SemesterCreate,
    session = Depends(get_async_session)
):
    return await createNewSemester(semester, session)

@router.delete("/{id}")
async def delete_semester(
    id: int,
    session = Depends(get_async_session)
):
    await deleteSemesterById(id, session)
    return {"message": f"Semester with id {id} deleted successfully"}