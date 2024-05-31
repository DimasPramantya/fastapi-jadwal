from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from model.slot_model import Slot as SlotModel
from schemas.slot_schema import Slot as SlotSchema, SlotCreate, SlotUpdate
from exceptions.entity_not_found_exception import EntityNotFoundException

async def addSlot(
    slot: SlotCreate,
    session: AsyncSession
) -> SlotModel:
    newSlot = SlotModel(
        start_time = slot.start_time,
        end_time = slot.end_time,
        is_lab_slot = slot.is_lab_slot
    )
    session.add(newSlot)
    await session.commit()
    await session.refresh(newSlot)
    return newSlot

async def deleteSlot(
    id: int,
    session: AsyncSession
):
    slot = await session.get(SlotModel, id)
    if not slot:
        raise EntityNotFoundException("Slot", id)
    await session.delete(slot)
    await session.commit()
    return

async def getSlotById(
    id: int,
    session: AsyncSession
)-> SlotModel:
    slot  = await session.get(SlotModel, id)
    if not slot:
        raise EntityNotFoundException("Slot", id)
    return slot

async def getSlotPageable(
    session: AsyncSession,
    skip: int = 0, 
    limit: int = 10, 
):
    result = await session.execute(
        select(SlotModel).offset(skip).limit(limit)
    )
    slot_list = result.scalars().all()
    return slot_list

async def updateSlot(
    id: int,
    slot: SlotUpdate,
    session: AsyncSession
):
    current_slot = await session.get(SlotModel, id)
    if not current_slot:
        raise EntityNotFoundException("Slot", id)
    current_slot.start = slot.start
    current_slot.end = slot.end
    current_slot.is_lab_slot = slot.is_lab_slot
    current_slot.day = slot.day
    session.add(current_slot)
    await session.commit()
    await session.refresh(current_slot)
    return current_slot
    
async def getSlotCount(session: AsyncSession) -> int:
    result = await session.execute(select(func.count(SlotModel.id)))
    return result.scalar_one()