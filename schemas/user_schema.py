from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    image_picture: str
    role: str
    fullname: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    is_email_verified: bool = True

    class Config:
        orm_mode = True
        from_attributes = True

def user_model_to_dict(user: User):
    return {
        "id": user.id,
        "nama_kelas": user.email,
        "role": user.role,
        "fullname": user.fullname,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }