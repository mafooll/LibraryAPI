from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str


class MessageResponse(BaseModel):
    message: str


class MeResponse(BaseModel):
    id: int


class LibrarianCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
