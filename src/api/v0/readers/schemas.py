from pydantic import BaseModel, EmailStr
from typing import Optional


class ReaderCreate(BaseModel):
    username: str
    email: EmailStr


class ReaderUpdate(BaseModel):
    # id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class ReaderRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
