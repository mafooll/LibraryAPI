from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


class ReaderCreate(BaseModel):
    username: str
    email: EmailStr


class ReaderUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class ReaderRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
