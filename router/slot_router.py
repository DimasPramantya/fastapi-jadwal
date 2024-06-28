from fastapi import APIRouter, Depends, HTTPException, Query

from util.db_connection import AsyncSession, get_async_session
from schemas.pagination_schema import Page
from schemas.slot_schema import Slot as SlotSchema, SlotCreate, SlotUpdate, slot_model_to_dict
from controller.slot_controller import *

router = APIRouter()

@router.get("/{id}", response_model=SlotSchema)
async def get_slot_by_id(
    id: int,
    session = Depends(get_async_session)
)->SlotSchema:
    return await getSlotById(id, session)

@router.put("/{id}", response_model=SlotSchema)
async def update_slot(
    id: int,
    slot: SlotUpdate,
    session = Depends(get_async_session)
)->SlotSchema:
    return await updateSlot(id, slot, session)

@router.delete("/{id}")
async def delete_slot(
    id: int,
    session = Depends(get_async_session)
):
    await deleteSlot(id, session)
    return {"message": f"Slot with id {id} deleted successfully"}

@router.get("", response_model=Page[SlotSchema])
async def get_slot_pageable(
    skip: int = Query(1, alias='page', description="Page number"),
    limit: int = Query(10, alias='size', description="Page size"),
    session = Depends(get_async_session)
)-> Page[SlotSchema]:
    if(skip > 0):
        offset = (skip - 1) * limit
    else:
        offset = 0
    slotList = await getSlotPageable(session, offset, limit)
    total = await getSlotCount(session)
    slotDict = [slot_model_to_dict(d) for d in slotList]
    return Page(total_elements=total, items=slotDict, size=limit, page=skip)

@router.post("", response_model = SlotSchema)
async def add_slot(
    slot: SlotCreate,
    session = Depends(get_async_session)
)-> SlotSchema:
    return await addSlot(slot,session)