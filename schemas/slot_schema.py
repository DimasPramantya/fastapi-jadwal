from pydantic import BaseModel, Field
from datetime import date, datetime, time
from typing import List, Optional

class SlotBase(BaseModel):
    start_time: time
    end_time: time
    is_lab_slot: bool
    day: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class SlotCreate(SlotBase):
    pass

class SlotUpdate(SlotBase):
    pass

class Slot(SlotBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

def slot_model_to_dict(slot: Slot):
     return {
        "id": slot.id,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "day": slot.day,
        "is_lab_slot": slot.is_lab_slot,
        "created_at": slot.created_at,
        "updated_at": slot.updated_at,
    }